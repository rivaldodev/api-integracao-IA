from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List, Dict, Optional
import re
import logging
from collections import Counter, defaultdict
import google.generativeai as genai
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    logger.info("Gemini 2.0 Flash configurado com sucesso!")
else:
    logger.warning("GEMINI_API_KEY não encontrada no arquivo .env. Funcionalidade de sentimento será limitada.")
    model = None

app = FastAPI(
    title="API de Análise de Texto",
    description="API para análise de texto com detecção de sentimento usando Google Gemini",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache para análises anteriores
analysis_cache: Dict[str, Dict] = {}
search_history: List[Dict] = []

# Stopwords em português
STOPWORDS = {
    'a', 'o', 'e', 'é', 'de', 'do', 'da', 'em', 'um', 'uma', 'para', 'com', 'não', 
    'na', 'no', 'se', 'que', 'por', 'mais', 'das', 'dos', 'como', 'mas', 'foi', 
    'ao', 'ele', 'sua', 'ou', 'ser', 'seu', 'à', 'até', 'pelo', 'pela', 'são', 
    'aos', 'às', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos',
    'quando', 'muito', 'nos', 'eu', 'você', 'eles', 'elas', 'já', 'só', 'tem',
    'pode', 'onde', 'vai', 'ainda', 'essa', 'este', 'esta', 'esse', 'todas',
    'todos', 'pela', 'pelo', 'sobre', 'antes', 'sempre', 'bem', 'também'
}

class TextAnalysisRequest(BaseModel):
    text: str
    
    @field_validator('text')
    @classmethod
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('O texto não pode estar vazio')
        return v

class WordFrequency(BaseModel):
    word: str
    frequency: int

class SentimentAnalysis(BaseModel):
    sentiment: str
    confidence: Optional[float] = None
    explanation: Optional[str] = None

class TextAnalysisResponse(BaseModel):
    word_count: int
    most_frequent_words: List[WordFrequency]
    sentiment_analysis: SentimentAnalysis
    analysis_timestamp: str

class SearchTermResponse(BaseModel):
    term: str
    found: bool
    occurrences: int
    last_analysis_timestamp: Optional[str] = None

def clean_text(text: str) -> str:
    """Remove pontuação e converte para minúsculas"""
    # Remove pontuação e caracteres especiais, mantém apenas letras e espaços
    cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
    # Remove espaços extras
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def get_word_frequencies(text: str, exclude_stopwords: bool = True) -> List[WordFrequency]:
    """Calcula a frequência das palavras no texto"""
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    
    if exclude_stopwords:
        words = [word for word in words if word not in STOPWORDS and len(word) > 2]
    
    word_counts = Counter(words)
    
    # Retorna as 5 palavras mais frequentes
    most_common = word_counts.most_common(5)
    
    return [WordFrequency(word=word, frequency=freq) for word, freq in most_common]

async def analyze_sentiment_with_gemini(text: str) -> SentimentAnalysis:
    """Analisa o sentimento do texto usando Google Gemini"""
    if not model:
        return SentimentAnalysis(
            sentiment="neutro",
            confidence=0.5,
            explanation="API key do Gemini não configurada"
        )
    
    try:
        prompt = f"""
        Analise o sentimento do seguinte texto em português e responda APENAS com um JSON no formato:
        {{"sentiment": "positivo/negativo/neutro", "confidence": 0.0-1.0, "explanation": "breve explicação"}}
        
        Texto para análise: "{text}"
        """
        
        response = model.generate_content(prompt)
        
        # Tenta extrair JSON da resposta
        response_text = response.text.strip()
        
        # Remove possíveis markdown ou texto extra
        if "```json" in response_text:
            json_part = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            json_part = response_text.split("```")[1]
        else:
            json_part = response_text
        
        try:
            result = json.loads(json_part)
            return SentimentAnalysis(
                sentiment=result.get("sentiment", "neutro"),
                confidence=float(result.get("confidence", 0.5)),
                explanation=result.get("explanation", "Análise realizada com Gemini")
            )
        except json.JSONDecodeError:
            # Fallback para análise simples baseada em palavras
            return simple_sentiment_analysis(text)
            
    except Exception as e:
        logger.error(f"Erro na análise de sentimento com Gemini: {e}")
        return simple_sentiment_analysis(text)

def simple_sentiment_analysis(text: str) -> SentimentAnalysis:
    """Análise de sentimento simples baseada em palavras-chave"""
    positive_words = {
        'bom', 'ótimo', 'excelente', 'maravilhoso', 'fantástico', 'incrível', 
        'adorável', 'perfeito', 'feliz', 'alegre', 'satisfeito', 'contente',
        'amor', 'sucesso', 'vitória', 'ganhar', 'positivo', 'bonito'
    }
    
    negative_words = {
        'ruim', 'péssimo', 'terrível', 'horrível', 'triste', 'deprimido',
        'raiva', 'ódio', 'problema', 'problemas', 'erro', 'erros', 'falha', 'defeito', 'negativo',
        'impossível', 'difícil', 'complicado', 'frustrado', 'chateado', 'infelizmente',
        'não', 'bugs', 'bug', 'urgentemente', 'resolvidos', 'esperado', 'funcionando'    }
    
    text_lower = clean_text(text)
    words = set(text_lower.split())
    
    # Verifica padrões negativos específicos
    negative_patterns = [
        "não está funcionando",
        "não funciona", 
        "cheio de problemas",
        "muitos problemas",
        "cheio de bugs",
        "muitos bugs"
    ]
    
    pattern_found = any(pattern in text_lower for pattern in negative_patterns)
    
    positive_count = len(words.intersection(positive_words))
    negative_count = len(words.intersection(negative_words))
    
    # Se encontrou padrão negativo, aumenta peso negativo
    if pattern_found:
        negative_count += 2    
    if positive_count > negative_count:
        sentiment = "positivo"
        confidence = min(0.85, 0.5 + (positive_count - negative_count) * 0.1)
        # Identifica palavras positivas encontradas
        positive_found = [word for word in words if word in positive_words]
        if positive_found:
            explanation = f"Texto contém palavras positivas como '{', '.join(positive_found[:3])}', indicando sentimento favorável"
        else:
            explanation = "Análise indica tom positivo baseado no contexto geral"
    elif negative_count > positive_count:
        sentiment = "negativo"  
        confidence = min(0.85, 0.5 + (negative_count - positive_count) * 0.1)
        # Identifica palavras negativas encontradas
        negative_found = [word for word in words if word in negative_words]
        patterns_found = [pattern for pattern in negative_patterns if pattern in text_lower]
        
        if patterns_found and negative_found:
            explanation = f"Texto expressa frustração com frases como '{patterns_found[0]}' e palavras negativas como '{', '.join(negative_found[:2])}'"
        elif patterns_found:
            explanation = f"Detectada expressão negativa: '{patterns_found[0]}'"
        elif negative_found:
            explanation = f"Presença de palavras negativas: '{', '.join(negative_found[:3])}'"
        else:
            explanation = "Análise indica tom negativo baseado no contexto"
    else:
        sentiment = "neutro"
        confidence = 0.5
        explanation = "Texto não apresenta palavras claramente positivas ou negativas, mantendo tom neutro"
    
    return SentimentAnalysis(
        sentiment=sentiment,
        confidence=confidence,
        explanation=explanation
    )

@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "API de Análise de Texto",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "POST /analyze-text",
            "search": "GET /search-term?term=palavra",
            "docs": "GET /docs"
        }
    }

@app.post("/analyze-text", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """
    Analisa um texto e retorna estatísticas básicas e análise de sentimento
    """
    try:
        text = request.text.strip()
        
        # Contagem de palavras
        word_count = len(clean_text(text).split())
        
        # Palavras mais frequentes
        most_frequent_words = get_word_frequencies(text)
        
        # Análise de sentimento
        sentiment_analysis = await analyze_sentiment_with_gemini(text)
        
        # Timestamp da análise
        timestamp = datetime.now().isoformat()
        
        # Armazena no cache para pesquisas futuras
        analysis_data = {
            "text": text,
            "word_count": word_count,
            "most_frequent_words": most_frequent_words,
            "sentiment_analysis": sentiment_analysis,
            "timestamp": timestamp
        }
        
        # Cache usando hash do texto como chave
        text_hash = str(hash(text))
        analysis_cache[text_hash] = analysis_data
        
        # Adiciona ao histórico
        search_history.append({
            "text": text,
            "timestamp": timestamp,
            "hash": text_hash
        })
        
        # Mantém apenas os últimos 100 registros
        if len(search_history) > 100:
            search_history.pop(0)
        
        logger.info(f"Análise realizada para texto de {word_count} palavras")
        
        return TextAnalysisResponse(
            word_count=word_count,
            most_frequent_words=most_frequent_words,
            sentiment_analysis=sentiment_analysis,
            analysis_timestamp=timestamp
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro na análise de texto: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/search-term", response_model=SearchTermResponse)
async def search_term(term: str):
    """
    Busca um termo nas análises anteriores
    """
    if not term.strip():
        raise HTTPException(status_code=400, detail="Termo de busca não pode estar vazio")
    
    term_lower = term.lower().strip()
    found = False
    total_occurrences = 0
    last_timestamp = None
    
    # Busca no histórico de análises
    for analysis_data in analysis_cache.values():
        text = analysis_data["text"]
        text_lower = clean_text(text)
        
        # Conta ocorrências do termo
        occurrences = text_lower.count(term_lower)
        if occurrences > 0:
            found = True
            total_occurrences += occurrences
            
            # Atualiza o timestamp da última análise que contém o termo
            if not last_timestamp or analysis_data["timestamp"] > last_timestamp:
                last_timestamp = analysis_data["timestamp"]
    
    logger.info(f"Busca realizada para termo '{term}': {total_occurrences} ocorrências")
    
    return SearchTermResponse(
        term=term,
        found=found,
        occurrences=total_occurrences,
        last_analysis_timestamp=last_timestamp
    )

@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "gemini_configured": model is not None,
        "cache_size": len(analysis_cache)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=os.getenv("APP_HOST", "0.0.0.0"), 
        port=int(os.getenv("APP_PORT", 3000))
    )
