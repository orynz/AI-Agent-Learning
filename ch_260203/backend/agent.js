const { tool_rule_check, tool_log, tool_db_search } = require("./tools");

const PRESETS = {
  todo_api: {
    title: "Node.js Todo API 점검",
    rules: [
      "엔드포인트/메서드가 명시되어야 합니다.",
      "요청/응답 예시가 있어야 합니다.",
      "DB 연결정보(DB_HOST/USER/PASSWORD/DB_NAME)가 있는지 확인합니다."
    ],
    db_probe_sql: "SELECT 1 AS ok"
  },
  compose_net: {
    title: "Docker Compose 네트워크/포트 점검",
    rules: [
      "서비스 이름 통신(DB_HOST=mysql 같은)이 맞는지 확인합니다.",
      "ports 매핑(host:container)이 맞는지 확인합니다.",
      "depends_on/healthcheck 유무를 확인합니다."
    ],
    db_probe_sql: "SELECT 1 AS ok"
  },
  db_charset: {
    title: "MySQL 한글/인코딩 점검",
    rules: [
      "DB/테이블/컬럼의 character set과 collation을 확인합니다.",
      "클라이언트 연결 설정(예: mysql2 charset)을 확인합니다.",
      "서버 설정과 클라이언트 설정의 불일치를 점검합니다."
    ],
    db_probe_sql: "SHOW VARIABLES LIKE 'character_set%';"
  }
};

// 진단 로그(trace) 누적 구조 추가
function pushTrace(trace, stage, message) {
  trace.push({
    ts: new Date().toISOString(),
    stage,
    message
  });
}

/**
 * 통합 에이전트 실행 함수
 * - 사용자 트레이스(trace)와 시스템 로깅(tool_log)을 동시에 수행
 * - 규칙 기반 검사 -> 안전성 검사 -> DB 진단 순으로 실행
 */
async function runAgent({ preset_id, question }) {
  const preset = PRESETS[preset_id];
  if (!preset) throw new Error("알 수 없는 preset_id 입니다.");

  // 1. 상태 및 트레이스 초기화
  const trace = []; // 사용자에게 보여줄 실행 경로
  const state = {   // 시스템 내부 로깅용 상태
    conversation_id: "c-" + Date.now(),
    preset_id,
    preset_title: preset.title,
    stage: "PLAN",
    evidence: [],
    attempts: 1
  };

  // ----------------------------------------------------------------
  // [STAGE: PLAN] 계획 수립
  // ----------------------------------------------------------------
  pushTrace(trace, "PLAN", "입력 분석 및 진단 계획을 수립합니다.");
  
  const plan = { target: preset.title, check_rules: true, check_db: !!preset.db_probe_sql };
  await tool_log({ stage: "PLAN", preset_id, conversation_id: state.conversation_id, plan });

  state.stage = "EXECUTE";

  // ----------------------------------------------------------------
  // [STAGE: EXECUTE] 1. 규칙 기반 정적 분석
  // ----------------------------------------------------------------
  pushTrace(trace, "PLAN", "프리셋 규칙 기반 진단을 시작합니다.");
  
  const ruleFindings = tool_rule_check(question, preset.rules);
  state.evidence.push({ type: "rules", data: ruleFindings });
  
  pushTrace(trace, "EXECUTE", `규칙 검증 수행: 의심 항목 ${ruleFindings.suspicious.length}건, 누락 ${ruleFindings.missing.length}건 발견`);

  await tool_log({
    stage: "EXECUTE",
    preset_id,
    conversation_id: state.conversation_id,
    ruleFindings
  });

  const missing = ruleFindings.missing || [];
  const suspicious = ruleFindings.suspicious || [];

  // ----------------------------------------------------------------
  // [CHECK] 정보 부족 시 조기 종료 (NEED_INFO)
  // ----------------------------------------------------------------
  if (missing.length >= 2) {
    pushTrace(trace, "VERIFY", "진단에 필요한 필수 정보가 부족합니다.");
    state.stage = "VERIFY";
    
    await tool_log({ stage: "VERIFY", preset_id, conversation_id: state.conversation_id, status: "NEED_INFO" });

    return {
      status: "NEED_INFO",
      answer: "정보가 부족하여 정확한 진단이 어렵습니다.\n" + missing.map(x => "- " + x).join("\n"),
      next_question: "관련된 로그 파일이나 설정 파일의 내용을 추가로 제공해주세요.",
      trace
    };
  }

  // ----------------------------------------------------------------
  // [CHECK] 안전성 검사 (Failover)
  // ----------------------------------------------------------------
  if (/rm\s+-rf|drop\s+database|format|mkfs/i.test(question)) {
    pushTrace(trace, "VERIFY", "파괴적인 명령어가 감지되어 진단을 중단합니다.");
    state.stage = "FAIL";
    
    await tool_log({ stage: "FAIL", preset_id, conversation_id: state.conversation_id, reason: "파괴적 명령 감지" });
    
    return {
      status: "FAIL",
      answer: "시스템 안전을 위해 파괴적인 명령어(삭제, 포맷 등)가 포함된 요청은 처리할 수 없습니다.",
      trace
    };
  }

  // ----------------------------------------------------------------
  // [STAGE: EXECUTE] 2. DB 동적 진단 (환경변수가 있을 경우)
  // ----------------------------------------------------------------
  let dbSummary = "진단 스킵";
  const hasDbEnv = !!(process.env.DB_HOST && process.env.DB_USER && process.env.DB_NAME);

  if (hasDbEnv && preset.db_probe_sql) {
    pushTrace(trace, "PLAN", "추가 진단 조건(DB)을 확인합니다.");
    try {
      const rows = await tool_db_search(preset.db_probe_sql);
      state.evidence.push({ type: "db", data: rows });
      
      const rowCount = Array.isArray(rows) ? rows.length : 0;
      dbSummary = `쿼리 성공(${rowCount} rows)`;
      pushTrace(trace, "EXECUTE", `DB 상태 점검 완료: ${dbSummary}`);
      
    } catch (e) {
      state.evidence.push({ type: "db_error", data: e.message });
      dbSummary = "쿼리 실패";
      pushTrace(trace, "EXECUTE", `DB 연결/쿼리 중 오류 발생: ${e.message}`);
      // DB 실패는 치명적이지 않다면 진행
    }
  } else {
    pushTrace(trace, "EXECUTE", "DB 환경 변수 미설정으로 심화 진단을 건너뜁니다.");
  }

  // ----------------------------------------------------------------
  // [STAGE: DONE] 최종 완료
  // ----------------------------------------------------------------
  pushTrace(trace, "VERIFY", "확인된 증거를 바탕으로 최종 진단을 내립니다.");
  state.stage = "DONE";
  
  await tool_log({ stage: "DONE", preset_id, conversation_id: state.conversation_id, status: "DONE" });

  // 최종 답변 생성
  // 최종 답변 생성
  const lines = [];
  lines.push("진단 결과");
  if (suspicious.length) lines.push("- 의심 항목: " + suspicious.join(", "));
  if (dbSummary) lines.push("- DB 진단: " + dbSummary);
  lines.push("");
  lines.push("확인 절차");
  lines.push("1) docker compose ps");
  lines.push("2) docker compose logs -f --tail=200 api");
  lines.push("3) docker compose logs -f --tail=200 mysql");
  lines.push("4) (호스트) DB 연결 확인: mysql -h 127.0.0.1 -P 3306 -uUSER -p");
  lines.push("5) (컨테이너 내부 통신) DB_HOST=mysql 로 통일되어 있는지 확인");
  lines.push("");
  lines.push("조치 방향");
  lines.push("- 누락/불일치가 있으면 .env와 compose 매핑을 먼저 수정합니다.");
  lines.push("- 컨테이너 내부 통신은 localhost 대신 서비스 이름(mysql)을 사용합니다.");
  
  return {
    status: "DONE",
    answer: lines.join("\n"),
    next_question: "위 1~5 결과를 붙여 넣으면 원인 확정 및 수정 단계로 진행합니다.",
    trace
  };
}


module.exports = { runAgent };
