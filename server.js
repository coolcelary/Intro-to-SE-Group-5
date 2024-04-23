const express = require("express")
const path = require("path")
const bodyParser = require("body-parser")
const { spawn } = require("child_process")
const cookieParser = require("cookie-parser")

const app = express()
// using port 3000 for now
const PORT = 3000

app.use(express.static(path.join(__dirname, "/frontend/")))
app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json());
app.use(cookieParser())


async function isApproved(sellerid){
  console.log(`./backend/Admin.py isapproved ${sellerid}`)
  const pythonProcess = spawn("python3", ["./backend/Admin.py", "isapproved", sellerid]) // Make admin page connection
  let valid = false
  await pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    if (result === "yes") {
      console.log(result)
      valid = true
    } else {
      console.log("no")
    }
  })
  return valid
}


// Admin login

app.get("/admin", (req, res) => {
  res.sendFile(path.join(__dirname, "/frontend/admin.html"))

})

app.post("/admin", (req, res) => {
  const { username, password } = req.body
  console.log(`./backend/Admin.py login ${username} ${password}`)
  const pythonProcess = spawn("python3", ["./backend/Admin.py", "login", username, password]) // Make admin page connection
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    if (result) {
      console.log(result)
      res.cookie("admin_auth", { maxAge: 900000, httpOnly: true })
      res.redirect("/admin_home")
    } else {
      console.log("invalid")
    }
  })

})

// Seller login

app.get("/seller", (req, res) => {
  res.sendFile(path.join(__dirname, "/frontend/seller.html"))
})

app.post("/seller", (req, res) => {
  const { username, password } = req.body
  console.log(`./backend/Seller.py login ${username} ${password}`)
  const pythonProcess = spawn("python3", ["./backend/Seller.py", "login", username, password])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    if (result && result !== "invalid") {
      console.log(result)
      res.cookie("sellerid", result, { maxAge: 900000, httpOnly: true });
      res.cookie("seller_auth", { maxAge: 900000, httpOnly: true })
      res.redirect("/sellers_view")
    } else {
      console.log("Login failed")
      res.redirect("/seller");
    }
  })

})

// Sellers page

app.get("/sellers_add", (req, res) => {
  if (req.cookies && req.cookies.seller_auth) {
    res.sendFile(path.join(__dirname, "/frontend/selleradd.html"))
  }
  else {
    res.redirect("/admin")
  }
})

app.get("/sellers_view", (req, res) => {
  if(req.cookies && req.cookies.sellerid && isApproved(req.cookies.sellerid)){
    console.log("here")
    res.sendFile(path.join(__dirname, "/frontend/sellerview.html"))
  }
  else{
    res.redirect("/seller")
  }
})

app.get("/sellers_edit", (req, res) => {
  if(req.cookies && req.cookies.seller_auth && isApproved(req.cookies.sellerid)){
    res.sendFile(path.join(__dirname, "/frontend/selleredit.html"))
  }
  else{
    res.redirect("/seller")
  }
})

app.get("/deleteProduct/:id", (req, res) => {
  const product_id = req.params.id
  if(!req.cookies || !req.cookies.seller_auth){
    res.status(400).json({valid:false})
  }
  console.log(`./backend/Seller.py delete ${product_id}`)
  const pythonProcess = spawn("python3", ["./backend/Seller.py", "delete", product_id])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    if (result) {
      res.status(200).json({valid:true})
    } else {
      res.status(500).json({valid:false})
    }
  })
})

app.post("/products", (req, res) => {
  const { name, price, category, image_url } = req.body;
  const seller_id = req.cookies.sellerid;
  console.log(`./backend/Seller.py add ${name} ${price} ${category} ${image_url} ${seller_id}`)
  const pythonProcess = spawn("python3", ["./backend/Seller.py", "add", name, price, category, image_url, seller_id])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result == "valid") {
      res.redirect("/sellers_view")
    } else {
      res.redirect("/sellers_add")
    }
  })
})

app.post("/products/edit", (req, res) => {
  if (req.cookies && req.cookies.seller_auth) {
    const { product_id, name, price, category, image_url } = req.body;
    const seller_id = req.cookies.sellerid;
    console.log(`./backend/Seller.py edit ${product_id} ${name} ${price} ${category} ${image_url} ${seller_id}`);
    const pythonProcess = spawn("python3", ["./backend/Seller.py", "edit", product_id, name, price, category, image_url, seller_id]);
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result);
      if (result == "valid") {
        res.redirect("/sellers_view");
      } else {
        res.redirect("/sellers_edit");
      }
    });
  } else {
    res.redirect("/admin");
  }
});

app.get("/seller_products", (req, res) => {
  const seller_id = req.cookies.sellerid;
  console.log(`python3 ./backend/Seller.py search "${seller_id}" `)
  const pythonProcess = spawn("python3", ["./backend/Seller.py", "search", seller_id])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(405).json([])
    }
  })
})

app.get("/productOrders/:id", (req, res) => {
  const product_id = req.params.id;
  console.log(`python3 ./backend/Order.py getorders "${product_id}" `)
  const pythonProcess = spawn("python3", ["./backend/Order.py", "getorders", product_id])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(405).json([])
    }
  })
})


// Admin Page

app.get("/admin_home", (req, res) => {
  if (!req.cookies || !req.cookies.admin_auth) {
    res.redirect("/login")
  }
  else {
    res.sendFile(path.join(__dirname, "/frontend/control.html"))
  }
})

app.get("/userlist", (req, res) => {
  if (!req.cookies || !req.cookies.admin_auth) {
    res.status(403).json([])
  }
  console.log(`python3 ./backend/Admin.py listall`)
  const pythonProcess = spawn("python3", ["./backend/Admin.py", "listall"])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(405).json([])
    }
  })
})

app.post("/ban/:id", (req, res) => {
  if(!req.cookies && !res.cookies.admin_auth){
    res.status(403).json({valid:false})
  } else{
    const id = req.params.id;
    console.log(`python3 ./backend/Admin.py ban ${id}`)
    const pythonProcess = spawn("python3", ["./backend/Admin.py", "ban", id])
    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString().trim();
      console.log(result)
      if (result == "valid") {
        res.status(200).json({valid:true})
      } else {
        res.status(405).json({valid:false})
      }
    })
  }
  })

app.get("/pending", (req,res) => {
  console.log(`python3 ./backend/Admin.py getpending `)
  const pythonProcess = spawn("python3", ["./backend/Admin.py", "getpending"])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(405).json([])
    }
  })
})

app.post("/approve/:id", (req, res) => {
  const id = req.params.id
  console.log(`python3 ./backend/Admin.py approve "${id}"`)
  const pythonProcess = spawn("python3", ["./backend/Admin.py", "approve", id])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json({valid:true})
    }
    else {
      res.status(405).json({valid:false})
    }
  })

})

app.get("/admin_products", (req, res) => {
  if(req.cookies && req.cookies.admin_auth){
    res.sendFile(path.join(__dirname, "/frontend/adminproducts.html"))
  } else{
    res.redirect("/admin")
  }
})




// Homepage

app.get("/", (req, res) => {
  if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "/frontend/homepage.html"))
  }
  else {
    res.redirect("/login")
  }
})

// Login page

app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "/frontend/login.html"))
})

app.post("/login", (req, res) => {
  const { username, password } = req.body;
  console.log(`./backend/Login.py login ${username} ${password}`)
  const pythonProcess = spawn("python3", ["./backend/Login.py", "login", username, password])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    if (result && result !== "invalid") {
      console.log(result)
      res.cookie("userid", result, { maxAge: 900000, httpOnly: true });
      res.cookie("authenticated", { maxAge: 900000, httpOnly: true })
      res.redirect("/")
    } else {
      console.log("invalid")
      res.redirect("/login")
    }
  })
})

// Registration page

app.get("/register", (req, res) => {
  res.sendFile(path.join(__dirname, "./frontend/registration.html"))
})

app.post("/register", (req, res) => {
  const { username, password, email, phone_number, customerCheckbox, sellerCheckbox } = req.body;
  const user_type = customerCheckbox === "1" ? "customer" : (sellerCheckbox === "1" ? "seller" : "customer");
  console.log(`python3 ./backend/Login.py register ${username} ${password} ${user_type} ${email} ${phone_number}`)
  const pythonProcess = spawn("python3", ["./backend/Login.py", "register", username, password, user_type, email, phone_number])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result == "True") {
      res.redirect("/login")
    }
    else {
      res.redirect("/login")
    }
  })
})

// Logout button

app.get("/logout", (req, res) => {
  res.clearCookie('authenticated')
  res.redirect("/login")
})

// About page

app.get("/about", (req, res) => {
  if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "./frontend/about-us.html"))
  }
  else {
    res.redirect("/login")
  }
})

// Products page

app.get("/products", (req, res) => {
  if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "./frontend/products.html"))
  }
  else {
    res.redirect("/login")
  }
})

app.get("/inventory", (req, res) => {
  let { name, category } = req.body;
  if (!name) name = "";
  if (!category) category = "";
  console.log(`python3 ./backend/Inventory.py search "${name}" "${category}"`)
  const pythonProcess = spawn("python3", ["./backend/Inventory.py", "search", name, category])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
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
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(405).json([])
    }
  })
})

app.delete("/blockProduct/:id", (req,res) => {
  const id = req.params.id
  console.log(`python3 ./backend/Admin.py block "${id}" `)
  const pythonProcess = spawn("python3", ["./backend/Admin.py", "block", id])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result === "valid") {
      res.status(200).json({valid:true})
    }
    else {
      res.status(405).json({valid:false})
    }
  })

})


// Cart page

app.get("/cart", (req, res) => {
  if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "./frontend/cart.html"))
  }
  else {
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
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(405).json([])
    }
  })
})

app.get("/cart_total", (req, res) => {
  const userid = req.cookies.userid;
  console.log(`python3 ./backend/Cart.py total "${userid}"`);
  const pythonProcess = spawn("python3", ["./backend/Cart.py", "total", userid]);
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result);
    if (!isNaN(result)) {
      res.status(200).json({ "total": parseFloat(result) });
    } else {
      res.status(500).json({ "error": "Failed to retrieve total price" });
    }
  });
});

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
      res.status(200).json({ "valid": true })
    }
    else {
      res.status(500).json({ "valid": false })
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
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(405).json([])
    }
  })
})

app.delete("/cartDecrement/:id", (req,res) => {
  const id = req.params.id
  const userid = req.cookies.userid
  console.log(`python3 ./backend/Cart.py decrement "${userid}" "${id}"`)
  const pythonProcess = spawn("python3", ["./backend/Cart.py", "decrement", userid, id])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json({valid:true})
    }
    else {
      res.status(405).json({valid:false})
    }
  })

})

// More info page

app.get("/more_info", (req, res) => {
  if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "./frontend/more.html"))
  }
  else {
    res.redirect("/login")
  }
})

app.get('/product/:id', (req, res) => {
  const id = req.params.id;
  console.log(`python3 ./backend/Inventory.py idsearch "${id}"`)
  const pythonProcess = spawn("python3", ["./backend/Inventory.py", "idsearch", id])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(405).json({})
    }
  })
});

app.get('/hasPurchased/:id', (req, res) => {
  const id = req.params.id;
  const userid = req.cookies.userid;
  console.log(`python3 ./backend/Order.py verify ${userid} ${id}`)
  const pythonProcess = spawn("python3", ["./backend/Order.py", "verify", userid, id])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result == "valid") {
      res.json({ valid: true })
    }
    else {
      res.json({ valid: false })
    }
  })

})

app.get("/review/:id", (req, res) => {
  const product_id = req.params.id;
  console.log(`python3 ./backend/review_module.py get ${product_id}`)
  const pythonProcess = spawn("python3", ["./backend/review_module.py", "get", product_id])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(500).json([])
    }
  })
})

app.post("/review", (req, res) => {
  const { productId, username, text, stars } = req.body;
  const userid = req.cookies.userid;
  console.log(`python3 ./backend/review_module.py add ${userid} ${productId} ${username} ${stars} "${text}"`)
  const pythonProcess = spawn("python3", ["./backend/review_module.py", "add", userid, productId, username, stars, `"${text}"`])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result == "valid\nvalid") {
      res.status(200).json({ valid: true });
    }
    else {
      res.status(400).json({ valid: false });
    }
  })

})

// Order History Page

app.get("/orderhistory", (req, res) => {
  if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "./frontend/orderhistory.html"))
  }
  else {
    res.redirect("/")
  }
})

app.get("/userOrders", (req, res) => {
  console.log(`python3 ./backend/Order.py get "${req.cookies.userid}"`)
  const userid = req.cookies.userid;
  const pythonProcess = spawn("python3", ["./backend/Order.py", "get", userid])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(405).json([])
    }
  })
})

app.get("/returnOrder/:id", (req, res) => {
  const product_id = req.params.id;
  const userid = req.cookies.userid
  console.log(`python3 ./backend/Order.py get "${product_id}" "${userid}"`)
  const pythonProcess = spawn("python3", ["./backend/Order.py", "return", product_id, userid])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json({valid:true})
    }
    else {
      res.status(405).json({valid:false})
    }
  })

})

// Account Information Page

app.get("/accountinfo", (req, res) => {
  if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "./frontend/accountinfo.html"))
  }
  else {
    res.redirect("/login")
  }
})

app.get("/accountdetails", (req, res) => {
  console.log(`python3 ./backend/Account.py"${req.cookies.userid}"`)
  const userid = req.cookies.userid;
  const pythonProcess = spawn("python3", ["./backend/Account.py", userid])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).json(JSON.parse(result.replace(/'/g, "\"")))
    }
    else {
      res.status(405).json([])
    }
  })
})

// Contact us page

app.get("/contact", (req, res) => {
  if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "./frontend/contact.html"))
  }
  else {
    res.redirect("/login")
  }
})

app.post("/contact", (req, res) => {
  const { name, email, message } = req.body;
  console.log(`python3 ./backend/Contact.py ${name} ${email} ${message}`)
  const pythonProcess = spawn("python3", ["./backend/Contact.py", name, email, `"${message}"`])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result) {
      res.status(200).send("Success");
    } else {
      res.status(500).send("Failure");
    }
  });
});


// Checkout page and button

app.get("/checkout", (req, res) => {
  if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "frontend/checkout.html"));
  }
  else {
    res.redirect("/login")
  }
})


app.post("/checkout", (req, res) => {
  const { name, address, email, card_number, expiry_date, card_holder_name, cvv } = req.body;
  const userid = req.cookies.userid;
  if (userid == undefined) {
    res.redirect("/login")
  }
  console.log(`python3 ./backend/Order.py ${userid} ${name} ${address} ${email} ${card_number} ${expiry_date} ${card_holder_name} ${cvv}`)
  const pythonProcess = spawn("python3", ["./backend/Order.py", "checkout", userid, name, address, email, card_number, expiry_date, card_holder_name, cvv])
  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString().trim();
    console.log(result)
    if (result == "valid") {
      res.send("<script>alert('Order placed'); window.location.href='/';</script>");
    }
    else {
      res.send("<script>alert('You have no items. Cannot checkout.')</script>")
    }
  })

})

// Compare Page

app.get("/compare", (req,res) => {
 if (req.cookies && req.cookies.authenticated) {
    res.sendFile(path.join(__dirname, "frontend/compare.html"));
  }
  else {
    res.redirect("/login")
  }
})

// Setup the server

app.listen(PORT, () => {
  console.log(`\nWelcome to LawnDepot.com! \nhttp://localhost:${PORT}`)
})
