const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = 3000;

// body-parser 설정: JSON과 URL-encoded 형식을 모두 처리할 수 있게 합니다.
app.use(bodyParser.json());
app.use(bodyParser.text());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    console.log("GET / ");
    res.end("Hello HS World!")
});

app.get('/hello', (req, res) => { // ?user=egoing&msg=hello
    console.log("GET / ");

    var user = req.query.user;
    var message = req.query.msg;
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end("GET /hello > " + user + " " + message)
});

// POST 요청 처리
app.post('/calc', (req, res) => {
    var num1 = Number(req.body.num1);
    var num2 = Number(req.body.num2);
    var operator = req.body.operator;
    var result = 0;

    if (operator == '+') {
        result = num1 + num2;
    } else if (operator == '-') {
        result = num1 - num2;
    } else if (perator == '/') {
        result = num1 / num2;
    } else {
        result = num1 * num2;
    }

    res.send(`POST /calc > ${num1} ${operator} ${num2} = ${result}`);
});

// const server = http.createServer(app)
app.listen(PORT, () => {
    console.log('Server running at http://localhost:3000/');
});

/*
curl.exe -X POST http://localhost:3000/calc `
-d "num1=1&num2=2&operator=-"
*/