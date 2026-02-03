const fs = require("fs");
const path = require("path");
const mysql = require("mysql2/promise");
require("dotenv").config();

// 문서/구현 계약 일치: tool_rule_check(text, preset_rules)
function tool_rule_check(text, preset_rules) {
  const missing = [];
  const suspicious = [];

  // 최소 재현에 필요한 근거 입력이 있는지 체크
  if (!/docker compose|docker-compose|compose/i.test(text)) missing.push("docker compose 실행 결과(ps/logs)가 필요합니다.");
  if (!/error|오류|Exception|ECONN|ER_/i.test(text)) missing.push("에러 로그 핵심 부분이 필요합니다.");
  if (!/DB_HOST|DB_USER|DB_NAME|MYSQL|3306|host|port/i.test(text)) missing.push("DB 연결 정보(DB_HOST/DB_USER/DB_NAME 등)가 필요합니다.");

  // 흔한 실수 패턴 감지
  if (/localhost:3306/i.test(text)) suspicious.push("컨테이너 내부 통신에 localhost를 쓰면 실패합니다(DB_HOST는 서비스 이름 권장).");
  if (/3306:3306/i.test(text) && /DB_HOST\s*=\s*127\.0\.0\.1/i.test(text)) suspicious.push("ports 매핑과 내부 통신 호스트가 섞여 있습니다.");

  return { missing, suspicious, rules: preset_rules };
}

async function tool_db_search(sql) {
  const conn = await mysql.createConnection({
    host: process.env.DB_HOST,
    port: Number(process.env.DB_PORT || "3306"),
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
  });
  const [rows] = await conn.execute(sql);
  await conn.end();
  return rows;
}

async function tool_log(event) {
  // 로그는 /logs 로 고정(Compose에서 볼륨 마운트)
  const logDir = process.env.LOG_DIR || "/logs";
  const logPath = path.join(logDir, "agent.log");
  if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });

  const line = JSON.stringify({ ts: new Date().toISOString(), ...event }) + "\n";
  fs.appendFileSync(logPath, line, "utf8");
}

module.exports = { tool_rule_check, tool_db_search, tool_log };
