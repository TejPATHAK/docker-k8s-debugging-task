const express = require('express');
const app = express();
const port = 3000;

const message = process.env.MESSAGE || "Hello from container!";

app.get('/', (req, res) => {
  res.send(message);
});

app.listen(port, '0.0.0.0', () => {
  console.log(`App running on port ${port}`);
});
