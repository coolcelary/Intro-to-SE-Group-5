const express = require("express")
const path = require("path")
const bodyParser = require("body-parser")
const { spawn } = require("child_process")
const cookieParser = require("cookie-parser")


const app = express()
const PORT = 3000

app.use(express.static(path.join(__dirname,"/frontend/")))
app.use(bodyParser.urlencoded({ extended: true }))
app.use(cookieParser())

app.get("/", (req, res) => {
  if (req.cookies && req.cookies.authenticated){
    res.sendFile(path.join(__dirname, "/frontend/homepage.html"))
  }
  else{
    res.redirect("/login")
  }
})

app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "/frontend/login.html"))
})

app.post("/login", (req, res) => {
  const { username, password } = req.body;
  console.log(username, password)
  const pythonProcess = spawn("python3", ["./backend/auth.py", "login", username, password])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    if (result == "True"){
      console.log("valid")
      res.cookie("authenticated", { maxAge: 900000, httpOnly: true})
      res.redirect("/")
    } else{
      console.log("invalid")
    }
  })
})

app.post("/logout", (req, res) => {
  res.clearCookie('authenticated')
  res.status(200)
})

app.listen(PORT, () =>{
  console.log(`http://localhost:${PORT}`)
})
