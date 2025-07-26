from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spacy
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Book Reader SpaCy API", version="1.0.0")

# Add CORS middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("SpaCy model loaded successfully")
except IOError:
    logger.error("SpaCy model not found. Please install: python -m spacy download en_core_web_sm")
    nlp = None

class SentenceRequest(BaseModel):
    sentence: str

class WordAnalysis(BaseModel):
    word: str
    lemma: str
    pos: str
    tag: str
    dep: str
    is_root: bool
    start_char: int
    end_char: int
    token_index: int

class SentenceAnalysisResponse(BaseModel):
    sentence: str
    root_word: str
    root_lemma: str
    root_pos: str
    root_start_char: int
    root_end_char: int
    root_token_index: int
    word_analysis: List[WordAnalysis]
    sentence_structure: str

@app.get("/")
async def root():
    return {"message": "Book Reader SpaCy API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "spacy_loaded": nlp is not None,
        "model": "en_core_web_sm" if nlp else "not loaded"
    }

@app.post("/analyze-sentence", response_model=SentenceAnalysisResponse)
async def analyze_sentence(request: SentenceRequest):
    if not nlp:
        raise HTTPException(status_code=500, detail="SpaCy model not loaded")
    
    if not request.sentence.strip():
        raise HTTPException(status_code=400, detail="Sentence cannot be empty")
    
    try:
        # Process the sentence with spaCy
        doc = nlp(request.sentence.strip())
        
        # Find the syntactic root (there's only one per sentence)
        root_token = None
        word_analysis = []
        
        for token in doc:
            is_root = token.dep_ == "ROOT"
            
            if is_root:
                root_token = token
            
            # Add detailed analysis for each word
            word_analysis.append(WordAnalysis(
                word=token.text,
                lemma=token.lemma_,
                pos=token.pos_,
                tag=token.tag_,
                dep=token.dep_,
                is_root=is_root,
                start_char=token.idx,
                end_char=token.idx + len(token.text),
                token_index=token.i
            ))
        
        if not root_token:
            raise HTTPException(status_code=500, detail="No root found in sentence")
        
        # Generate sentence structure description
        structure_parts = [f"Root: {root_token.text} ({root_token.pos_})"]
        
        # Find key dependents
        for child in root_token.children:
            if child.dep_ == "nsubj":
                structure_parts.append(f"Subject: {child.text}")
            elif child.dep_ == "dobj":
                structure_parts.append(f"Object: {child.text}")
            elif child.dep_ in ["amod", "advmod"]:
                structure_parts.append(f"Modifier: {child.text}")
        
        sentence_structure = " | ".join(structure_parts)
        
        return SentenceAnalysisResponse(
            sentence=request.sentence,
            root_word=root_token.text,
            root_lemma=root_token.lemma_,
            root_pos=root_token.pos_,
            root_start_char=root_token.idx,
            root_end_char=root_token.idx + len(root_token.text),
            root_token_index=root_token.i,
            word_analysis=word_analysis,
            sentence_structure=sentence_structure
        )
        
    except Exception as e:
        logger.error(f"Error analyzing sentence: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing sentence: {str(e)}")

@app.post("/find-root")
async def find_root(request: SentenceRequest):
    """Simplified endpoint that returns just the syntactic root with position"""
    if not nlp:
        raise HTTPException(status_code=500, detail="SpaCy model not loaded")
    
    try:
        doc = nlp(request.sentence.strip())
        
        # Find the single syntactic root
        for token in doc:
            if token.dep_ == "ROOT":
                return {
                    "sentence": request.sentence,
                    "root_word": token.text,
                    "root_lemma": token.lemma_,
                    "root_pos": token.pos_,
                    "start_char": token.idx,
                    "end_char": token.idx + len(token.text),
                    "token_index": token.i
                }
        
        raise HTTPException(status_code=500, detail="No root found in sentence")
        
    except Exception as e:
        logger.error(f"Error finding root: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error finding root: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)