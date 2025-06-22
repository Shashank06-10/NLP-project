const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { extractKeyPhrases, analyzePhraseContext } = require('./nlp-utils');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/analyzer', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'analyzer.html'));
});

app.post('/analyze', (req, res) => {
  const text = req.body.text || '';
  
  if (!text) {
    return res.status(400).json({ error: 'No text provided' });
  }
  
  // Extract key phrases
  const keyPhrases = extractKeyPhrases(text);
  
  // Get context for top phrases
  const contextInsights = analyzePhraseContext(text, keyPhrases);
  
  // Calculate text statistics
  const wordCount = text.split(/\s+/).filter(word => word.length > 0).length;
  const charCount = text.length;
  
  return res.json({
    key_phrases: keyPhrases,
    context_insights: contextInsights,
    stats: {
      word_count: wordCount,
      char_count: charCount
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Open http://localhost:${PORT} in your browser`);
});