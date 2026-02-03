const express = require("express");
const path = require("path");
const { runAgent } = require("./agent");

const app = express();
app.use(express.json({ limit: "2mb" }));

// 컨테이너 내부에 /app/web 이 포함되도록 Dockerfile에서 COPY 합니다.
app.use(express.static(path.join(__dirname, "..", "web")));

app.post("/api/coach", async (req, res) => {
  try {
    const { preset_id, question } = req.body || {};
    if (!preset_id || !question) {
      return res.status(400).json({ error: "preset_id와 question이 필요합니다." });
    }
    const result = await runAgent({ preset_id, question });
    return res.json(result);
  } catch (e) {
    return res.status(500).json({ error: e.message || "서버 오류" });
  }
});

app.listen(3000, () => console.log("OK: http://localhost:3000"));
