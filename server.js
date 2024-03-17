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
app.use(bodyParser.json());

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
  console.log(`./backend/Login.py login ${username} ${password}`)
  const pythonProcess = spawn("python3", ["./backend/Login.py", "login", username, password])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    if (result) {
      console.log(result)
      res.cookie("userid", result, { maxAge: 900000, httpOnly: true });
      res.cookie("authenticated", { maxAge: 900000, httpOnly: true })
      res.redirect("/")
    } else {
      console.log("invalid")
    }
  })
})

app.get("/logout", (req, res) => {
  res.clearCookie('authenticated')
  res.redirect("/login")
})

app.get("/register", (req, res) => {
  res.sendFile(path.join(__dirname, "./frontend/registration.html"))
})

app.post("/register", (req, res) => {
  const { username, password, email, phone} = req.body;
  console.log(phone)
  const user_type = "customer"
  const pythonProcess = spawn("python3", ["./backend/Login.py", "register", username, password, user_type, email, phone])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result == "True") {
      res.status(200).json({ "valid": true })
    }
    else {
      res.status(405).json({ "valid": false })
    }
  })
})

app.get("/about", (req, res) => {
  if(req.cookies && req.cookies.authenticated){
    res.sendFile(path.join(__dirname, "./frontend/about-us.html"))
  }
  else{
    res.redirect("/login")
  }
})

app.get("/products", (req, res) => {
  if(req.cookies && req.cookies.authenticated){
    res.sendFile(path.join(__dirname, "./frontend/products.html"))
  }
  else{
    res.redirect("/login")
  }
})

app.get("/inventory", (req, res) => {
    let { name, category } = req.body;
    if(!name) name = "";
    if(!category) category = "";
    console.log(`python3 ./backend/Inventory.py search "${name}" "${category}"`)
    const pythonProcess = spawn("python3", ["./backend/Inventory.py", "search", name, category])
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result)
      if (result) {
        res.status(200).json(JSON.parse(result.replace(/'/g,"\"")))
      }
      else {
        res.status(405).json([])
      }
    })
})

app.get("/search", (req, res) => {
    const query = req.query.q
    console.log(`python3 ./backend/Inventory.py search "${query}" ""`)
    const pythonProcess = spawn("python3", ["./backend/Inventory.py", "search", query, ""])
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result)
      if (result) {
        res.status(200).json(JSON.parse(result.replace(/'/g,"\"")))
      }
      else {
        res.status(405).json([])
      }
    })
})

app.get("/cart_search", (req, res) => {
    const query = req.query.q
    const userid = req.cookies.userid
    console.log(`python3 ./backend/Cart.py search "${userid}" "${query}"`)
    const pythonProcess = spawn("python3", ["./backend/Cart.py", "search", userid, query])
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result)
      if (result) {
        res.status(200).json(JSON.parse(result.replace(/'/g,"\"")))
      }
      else {
        res.status(405).json([])
      }
    })
})



app.get("/cart", (req, res) => {
  if(req.cookies && req.cookies.authenticated){
    res.sendFile(path.join(__dirname, "./frontend/cart.html"))
  }
  else{
    res.redirect("/login")
  }
})

app.get("/cart_items", (req, res) => {
    console.log(`python3 ./backend/Cart.py get "${req.cookies.userid}"`)
    const userid = req.cookies.userid;
    const pythonProcess = spawn("python3", ["./backend/Cart.py", "searchid", userid])
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result)
      if (result) {
        res.status(200).json(JSON.parse(result.replace(/'/g,"\"")))
      }
      else {
        res.status(405).json([])
      }
    })
})

app.post("/cart", (req, res) => {
  const { itemid } = req.body
  const userid = req.cookies.userid
  console.log(`python3 ./backend/Cart.py add ${userid} ${itemid}`)
  const pythonProcess = spawn("python3", ["./backend/Cart.py", "add", userid, itemid])
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result)
      if (result == "valid") {
        res.status(200)
      }
      else {
        res.status(500)
      }
    })
})

app.delete("/cart", (req, res) => {
  const { itemid } = req.body
  const userid = req.cookies.userid
  console.log(`python3 ./backend/Cart.py remove ${userid} ${itemid}`)
  const pythonProcess = spawn("python3", ["./backend/Cart.py", "remove", userid, itemid])
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result)
      if (result == "valid") {
        res.status(200).json({"valid":true})
      }
      else {
        res.status(500).json({"valid":false})
      }
    })
})

app.get('/product/:id', (req, res) => {
    const id = req.params.id;
    console.log(`python3 ./backend/Inventory.py idsearch "${id}"`)
    const pythonProcess = spawn("python3", ["./backend/Inventory.py", "idsearch", id])
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result)
      if (result) {
        res.status(200).json(JSON.parse(result.replace(/'/g,"\"")))
      }
      else {
        res.status(405).json({})
      }
    })
});


app.get("/contact", (req, res) => {
  if(req.cookies && req.cookies.authenticated){
    res.sendFile(path.join(__dirname, "./frontend/contact.html"))
  }
  else{
    res.redirect("/login")
  }
})

app.post("/contact", (req, res) => {
  const {name, email, message} = req.body;
  console.log(`python3 ./backend/Contact.py ${name} ${email} ${message}`)
  const pythonProcess = spawn("python3", ["./backend/Contact.py", name, email, `"${message}"`])
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result)
      if (result == "message OK") {
        res.status(200)
      }
      else {
        res.status(500)
      }
    })
})

app.get("/checkout", (req, res) => {
  const userid = req.cookies.userid
  console.log(`python3 ./backend/Order.py ${userid}`)
  const pythonProcess = spawn("python3", ["./backend/Order.py", "checkout", userid])
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result)
      if (result == "valid") {
        res.redirect("/")
      }
      else {
        res.redirect("/error")
      }
    })

})


app.listen(PORT, () => {
  console.log(`http://localhost:${PORT}`)
})
