const express = require("express")
const app = express()
const mysql = require("mysql")

//change depending on your env variables
const db = mysql.createPool({
    host:  'localhost',
    user: 'root',
    database: 'lids-db',
    port: '3001'
});

//app.get("/", (req, res) => {
   //change depending on path
//});

app.listen(3002, () =>{
    console.log("running on port 3002");
})