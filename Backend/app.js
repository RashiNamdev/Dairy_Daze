const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const { Client } = require('pg'); // PostgreSQL client
const cors = require('cors'); // Import CORS package

app.use(cors()); // Enable CORS for all routes
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Connect to PostgreSQL
const client = new Client({
  host: 'localhost',
  port: 5432, // default PostgreSQL port
  user: 'postgres',
  password: 'Shiksha@30', 
  database: 'Dairy_Management', 
});

client.connect();

// Define route for handling customer registration
app.post('/register', async (req, res) => {
  const { name, email, phone, password } = req.body;

  // You can use SQL to insert this data into your database
  const query = `
  INSERT INTO customers (full_name, email, phone_number, password)
  VALUES ($1, $2, $3, $4)
`;
  const values = [name, email, phone, password];

  try {
    await client.query(query, values); // Execute the query
    res.status(200).json({ message: 'Registered successfully' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Error registering customer' });
  }
});

// Start server
app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
