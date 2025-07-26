# Book Reader SpaCy Backend

FastAPI backend service for finding syntactic roots in sentences using spaCy NLP.

## Features

- 🔍 **Root Word Finding**: Identifies the syntactic root of any sentence
- 📝 **Full Sentence Analysis**: Detailed POS tagging and dependency parsing
- 🚀 **Fast Processing**: Handles thousands of sentences per second
- 🐳 **Docker Ready**: Easy deployment with containerization

## API Endpoints

### `GET /health`
Health check endpoint to verify service status and spaCy model loading.

### `POST /find-root`
Returns the syntactic root of a sentence.

**Request:**
```json
{
  "sentence": "The cat sits on the mat"
}
```

**Response:**
```json
{
  "sentence": "The cat sits on the mat",
  "root_word": "sits",
  "root_lemma": "sit", 
  "root_pos": "VERB",
  "start_char": 8,
  "end_char": 12,
  "token_index": 2
}
```

### `POST /analyze-sentence`
Full sentence analysis with all words and dependencies.

**Request:**
```json
{
  "sentence": "The cat sits on the mat"
}
```

**Response:**
```json
{
  "sentence": "The cat sits on the mat",
  "root_word": "sits",
  "root_lemma": "sit",
  "root_pos": "VERB",
  "root_start_char": 8,
  "root_end_char": 12,
  "root_token_index": 2,
  "word_analysis": [
    {
      "word": "sits",
      "lemma": "sit",
      "pos": "VERB",
      "tag": "VBZ",
      "dep": "ROOT",
      "is_root": true,
      "start_char": 8,
      "end_char": 12,
      "token_index": 2
    }
  ],
  "sentence_structure": "Root: sits (VERB) | Subject: cat | Object: mat"
}
```

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```

3. **Test the API:**
   ```bash
   curl -X POST "http://localhost:8000/find-root" \
        -H "Content-Type: application/json" \
        -d '{"sentence": "I love reading books"}'
   ```

## Docker Deployment

1. **Build image:**
   ```bash
   docker build -t book-reader-spacy-api .
   ```

2. **Run container:**
   ```bash
   docker run -p 8000:8000 book-reader-spacy-api
   ```

## Deploy to Render

1. Fork/clone this repository
2. Create new Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

## Technology Stack

- **FastAPI**: Modern Python web framework
- **spaCy**: Industrial-strength NLP library
- **uvicorn**: ASGI server implementation
- **Docker**: Containerization platform

## Use Cases

Perfect for:
- 📚 Reading apps that need sentence analysis
- 🎯 Educational tools for grammar learning
- 🔍 Text processing pipelines
- 📖 Language learning applications

## License

MIT License - feel free to use in your projects!