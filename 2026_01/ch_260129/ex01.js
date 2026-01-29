let http = require('http');

http.createServer(function (req, res) {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end('Hello World\n');
}).listen(3000);

console.log('Server running at http://localhost:3000/');

// 터미널 실행
// node ex01.js