const express = require('express');

app = express();
app.set('views', __dirname + "/views");
app.set('view engine', 'ejs');
app.set('port', 3000);

var cnt = 0;
var users = [];

app.get("/", function(req, res){
    res.render("home");
});

app.get("/list", function(req, res){
    console.log("GET /list");
    res.render("list", {users});
});

app.get("/input", (req, res) => {
    console.log("GET /input");

    var uid = cnt++;
    var name = req.query.name;
    var email = req.query.email;

    users.push({uid:uid, name:name, email:email});

    console.log(users)
    res.redirect("/list");
});

app.get("/detail", (req, res) => {
    console.log("GET /detail");
    var uid = req.query.uid;
    for(let i=0; i<users.length; i++){
        if(users[i].uid == uid) {
            var name = users[i].name;
            var email = users[i].email;
            break;
        }
    }

    console.log("UID = "+uid)
    res.render("detail", {users, uid, name, email});
});

app.get("/modify", (req, res) => {
    console.log("GET /modify");
    var uid = req.query.uid;
    for(let i=0; i<users.length; i++){
        if(users[i].uid == uid){
            var name = users[i].name;
            var email = users[i].email;
            break;
        }
    }

    console.log("UID = "+uid)
    res.render("modify", {users, uid, name, email});
});

app.get("/modify_ok", (req, res) => {
    console.log("GET /modify_ok");
    var uid = req.query.uid;
    var name = req.query.name;
    var email = req.query.email;
    for(let i=0; i<users.length; i++){
        if(users[i].uid == uid){
            users[i].name = name;
            users[i].email = email;
            break;
        }
    }
    console.log("UID = "+uid)
    res.redirect("/list");
});

app.get("/delete", (req, res) => {
    console.log("GET /delete");
    var uid = req.query.uid;
    for(let i=0; i<users.length; i++){
        if(users[i].uid == uid){
            users.splice(i, 1);
            break;
        }
    }
    console.log("UID = "+uid)
    res.redirect("/list");
});

app.listen(app.get('port'), () => {
    console.log(`http://localhost:${app.get('port')}`);
});