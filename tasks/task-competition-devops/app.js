require('dotenv').config();
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const appName = process.env.APP_NAME || 'CompetitionLevelApp';
app.get('/', (req, res) => {
  res.send(`Hello from ${appName}!`);
});
app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running on port ${port}`);
});
