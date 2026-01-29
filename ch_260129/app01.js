const express = require('express');
const app = express();
const PORT = 3030;
app.set('port', PORT);

// 뷰 엔진 설정 
app.set("views", __dirname + '/views');
app.set("view engine", "ejs");

app.get("/", function(req, res) {
    var user = req.query.user ? req.query.user : "테스트";
    var msg = req.query.msg ? req.query.msg : "테스트 메시지";
    var age = req.query.age ? req.query.age : "20";

    // 응답 페이지를 ejs 페이지로 변경
    res.app.render("index", {user: user, msg: msg, age: age}, function(err, html){ // render(ejs 파일명, 전달할 데이터, 콜백함수)
        if(err) throw err;
        res.end(html);
    });
});
app.get("/hello", function(req, res){
    var user = req.query.user;
    var msg = req.query.msg;
    var age = req.query.age;
    res.send("<h1>" + user + "님 안녕하세요</h1>" + msg + "<br>" + age + "살");    
})
// app.get("/hello", function(req, res) {
//     // 응답 페이지를 ejs 페이지로 변경
//     res.app.render("", {}, function(err, html){ // render(ejs 파일명, 전달할 데이터, 콜백함수)
//         if(err) throw err;
//         res.end(html);
//     });
// });

app.listen(app.get('port'), function(){
    console.log("Server On - http://localhost:" + app.get('port'));
});