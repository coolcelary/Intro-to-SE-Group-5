const express = require("express")
const path = require("path")
const bodyParser = require("body-parser")
const { spawn } = require("child_process")



const app = express()
const PORT = 3000

app.use(express.static(path.join(__dirname,"../frontend/")))
app.use(bodyParser.urlencoded({ extended: true }))

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "../frontend/homepage.html"))
})

app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "../frontend/login.html"))
})

app.post("/login", (req, res) => {
  const { username, password } = req.body;
  console.log(username, password)
})

app.listen(PORT, () =>{
  console.log(`http://localhost:${PORT}`)
})
