const express = require('express');

app = express();
app.set('views', __dirname + "/views");
app.set('view engine', 'ejs');
app.set('port', 3000);

app.get("/", function(req, res){
    res.render("form");
});

var users = [];

app.get("/result", function(req, res){

    var name = req.query.name;
    var email = req.query.email;
    
    users.push({name:name, email:email});

    res.render("result", {name, email, users});
});

app.listen(app.get('port'), () => {
    console.log(`http://localhost:${app.get('port')}`);
});