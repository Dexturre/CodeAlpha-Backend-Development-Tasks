const express = require('express');
const { nanoid } = require('nanoid');
const { Low } = require('lowdb');
const { JSONFile } = require('lowdb/node');
const path = require('path');

const app = express();
const port = 5000;

// Setup lowdb to use JSON file
const file = path.join(__dirname, 'db.json');
const adapter = new JSONFile(file);
const defaultData = { urls: [] };
const db = new Low(adapter, defaultData);

// Middleware to parse JSON bodies
app.use(express.json());

// Middleware to serve static files
app.use(express.static(path.join(__dirname)));

// Root route to serve index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// API endpoint to shorten URL
app.post('/shorten', async (req, res) => {
  try {
    const { longUrl } = req.body;
    if (!longUrl) {
      return res.status(400).json({ error: 'longUrl is required' });
    }

    // Generate unique short code
    const shortCode = nanoid(7);

    // Save to database
    await db.read();
    db.data.urls.push({ shortCode, longUrl });
    await db.write();

    // Return short URL
    const shortUrl = `${req.protocol}://${req.get('host')}/${shortCode}`;
    res.json({ shortUrl });
  } catch (error) {
    console.error('Error shortening URL:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Test route to verify server is working
app.get('/test', (req, res) => {
  res.send('Test route working');
});

// Redirect route (catch all other GET requests except above)
app.get('/:shortCode', async (req, res) => {
  try {
    const { shortCode } = req.params;
    await db.read();
    const urlEntry = db.data.urls.find(u => u.shortCode === shortCode);
    if (urlEntry) {
      res.redirect(urlEntry.longUrl);
    } else {
      res.status(404).send('Short URL not found');
    }
  } catch (error) {
    console.error('Error redirecting:', error);
    res.status(500).send('Internal server error');
  }
});

// Initialize database and start server
db.read().then(() => {
  app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
  });
}).catch((error) => {
  console.error('Error initializing database:', error);
  process.exit(1);
});
