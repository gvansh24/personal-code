const express = require("express");
const path = require('path')
const port = 8000;
const db = require("./config/mongoose")
const Contact = require("./models/contact")
const app = express();


app.set("view engine",'ejs');
app.set('views',path.join(__dirname,'views'));
app.use(express.urlencoded())

var contactsList = [
    {
        name:"vansh",
        number:"8745045429"
    },
    {
        name:"mahima",
        number:"9891144453"
    },
    {
        name:"hemlata",
        number:"8750524105"
    }
]

app.get('/',function(req,res){
    // console.log(req)
    // res.send("hello world")
    Contact.find({},function(err,contacts){
      if(err){
        console.log("Error fetching contacts from db");
        return;
      }
      res.render('home',{
        title:"Contacts list",
        contact_list:contacts
    })
    });
    
});
app.post("/create-contact",function(req,res)
{
    // contactsList.push(
    //     {
    //         name: req.body.name,
    //         number: req.body.number
    //     }
    // )
    Contact.create({
        name:req.body.name,
        number:req.body.number
    },function(err,newContact){
        if (err)
        {console.log("error creating the contact again");
        return;} 
        console.log("********",newContact);
        return res.redirect("/")      
    });
    
});
//for deleting the contact
app.get("/delete",function(req,res){
    //get the id from the query url 
    let id = req.query.id;
    //find the contact in the database using the id and delete it
    Contact.findByIdAndDelete(id,function(err){
        if(err){
            console.log("error deleting the contact from the database")
            return;  
        }
        return res.redirect("back");
    })

    
    
});


app.listen(port,function(err){
    if (err)
    {
        console.log("error alert",err)
    }
    else
        console.log("server running on port :",port) 
})