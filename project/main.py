from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple
from rake_nltk import Rake

app = FastAPI()

# Allow frontend on localhost:5500
origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_text(req: TextRequest):
    print('hello')
    text = req.text.strip()
    if not text:
        return {"key_phrases": [], "context_insights": [], "stats": {"word_count": 0, "char_count": 0}}

    rake = Rake()
    rake.extract_keywords_from_text(text)
    ranked_phrases = rake.get_ranked_phrases_with_scores()

    word_count = len(text.split())
    char_count = len(text)

    key_phrases: List[Tuple[str, int]] = []
    context_insights: List[Tuple[str, int, str]] = []

    for score, phrase in ranked_phrases:
        count = text.lower().count(phrase.lower())
        key_phrases.append((phrase, count))

        sentence = next((s for s in text.split('.') if phrase.lower() in s.lower()), "").strip()
        if sentence:
            context_insights.append((phrase, count, sentence + "."))

    return {
        "key_phrases": key_phrases,
        "context_insights": context_insights,
        "stats": {
            "word_count": word_count,
            "char_count": char_count
        }
    }