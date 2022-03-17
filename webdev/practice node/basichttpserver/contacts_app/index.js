const express = require("express");
const path = require('path')
const port = 8000;
app = express();


app.set("view engine",'ejs');
app.set('views',path.join(__dirname,'views'));

app.get('/',function(req,res){
    // console.log(req)
    // res.send("hello world")
    res.render('home',{title:"i am ironman"})
});


app.listen(port,function(err){
    if (err)
    {
        console.log("error alert",err)
    }
    else
        console.log("server running on port :",port) 
})