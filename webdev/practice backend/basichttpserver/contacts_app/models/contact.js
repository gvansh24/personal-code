//import mongoose
const mongoose = require("mongoose");
//setup mongoose schema
const contactSchema = new mongoose.Schema({
    name:{
        type :String,
        required :true
    },
    number:{
        type:String,
        required:true
    }
}); 
const Contact = mongoose.model("Contact",contactSchema) 
module.exports = Contact;