const express = require('express');
const app = express();
const PORT = 3000;
app.set('port', PORT);

var html = `
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Home</h1>
    <form action="/hello" method="get">
        <input type="text", name="user", placeholder="이름">
        <input type="text", name="msg", placeholder="메시지">
        <input type="text", name="age", placeholder="나이">
        <button type="submit">전송</button>
    </form>
</body>
</html>
`
app.get("/", function(req, res) {
    res.send(html);
});

app.get("/hello", function(req, res){
    var user = req.query.user ? req.query.user : "AI 에이전트"
    var msg = req.query.msg ? req.query.msg : "X"
    var age = req.query.age ? req.query.age : "X"
    console.log(user, msg, age);
    res.send(`
        <h1>Hello World! </h1>
        <p>이름: ${user}</p>
        <p>메시지: ${msg}</p>
        <p>나이: ${age}</p>
        `
    );
});

app.listen(app.get('port'), function(){
    console.log("Server On - http://localhost:" + app.get('port'));
});