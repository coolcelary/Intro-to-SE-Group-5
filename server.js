const express = require("express")
const path = require("path")
const bodyParser = require("body-parser")
const { spawn } = require("child_process")
const cookieParser = require("cookie-parser")

// comment here:
const app = express()
const PORT = 3000

app.use(express.static(path.join(__dirname, "/frontend/")))
app.use(bodyParser.urlencoded({ extended: true }))
app.use(cookieParser())

app.get("/", (req, res) => {
  if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "/frontend/homepage.html"))
  }
  else {
    res.redirect("/login")
  }
})

app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "/frontend/login.html"))
})

app.post("/login", (req, res) => {
  const { username, password } = req.body;
  console.log(`./backend/Login_Module.py login ${username} ${password}`)
  const pythonProcess = spawn("python3", ["./backend/Login_Module.py", "login", username, password])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    if (result == "True") {
      console.log("valid")
      res.cookie("authenticated", { maxAge: 900000, httpOnly: true })
      res.redirect("/")
    } else {
      console.log("invalid")
    }
  })
})

app.post("/logout", (req, res) => {
  res.clearCookie('authenticated')
  res.status(200)
})

app.post("/register", (req, res) => {
  const { username, password, user_type, email, phone } = req.body;
  const pythonProcess = spawn("python3", ["./backend/Login_Module.py", "register", username, password, user_type, email, phone])
  pythonProcess.on('data', (data) => {
    const result = data.toString().trim();
    if (result == "True") {
      res.status(200).json({ "valid": true })
    }
    else {
      res.status(405).json({ "valid": false })
    }
  })
})

app.listen(PORT, () => {
  console.log(`http://localhost:${PORT}`)
})
