const company = "나노AI";
const _status = "상승";

const report = `현재 ${company}의 주가는 시장분석 결과 ${_status}세 입니다.`;

console.log(report);

let html = `새로 추가된 아이템[${company}]
<input> type="button" value="삭제" onclick="removeItem(${_status})"/>`


console.log(html);
