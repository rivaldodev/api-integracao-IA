"""
Testes para a API de Análise de Texto
"""

import pytest
from fastapi.testclient import TestClient
from main import app, clean_text, get_word_frequencies, simple_sentiment_analysis

client = TestClient(app)

def test_root_endpoint():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data

def test_health_endpoint():
    """Testa o endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "gemini_configured" in data
    assert "cache_size" in data

def test_analyze_text_valid():
    """Testa análise de texto válido"""
    test_text = "Este é um texto de exemplo muito interessante e positivo para testar nossa API incrível"
    
    response = client.post(
        "/analyze-text",
        json={"text": test_text}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verifica estrutura da resposta
    assert "word_count" in data
    assert "most_frequent_words" in data
    assert "sentiment_analysis" in data
    assert "analysis_timestamp" in data
    
    # Verifica tipos
    assert isinstance(data["word_count"], int)
    assert isinstance(data["most_frequent_words"], list)
    assert isinstance(data["sentiment_analysis"], dict)
    
    # Verifica contagem de palavras
    assert data["word_count"] > 0
    
    # Verifica palavras mais frequentes
    assert len(data["most_frequent_words"]) <= 5
    for word_freq in data["most_frequent_words"]:
        assert "word" in word_freq
        assert "frequency" in word_freq
        assert isinstance(word_freq["frequency"], int)
    
    # Verifica análise de sentimento
    sentiment = data["sentiment_analysis"]
    assert "sentiment" in sentiment
    assert "confidence" in sentiment
    assert sentiment["sentiment"] in ["positivo", "negativo", "neutro"]

def test_analyze_text_empty():
    """Testa análise com texto vazio"""
    response = client.post(
        "/analyze-text",
        json={"text": ""}
    )
    
    assert response.status_code == 422

def test_analyze_text_whitespace():
    """Testa análise com apenas espaços"""
    response = client.post(
        "/analyze-text",
        json={"text": "   "}
    )
    
    assert response.status_code == 422

def test_search_term_found():
    """Testa busca de termo após análise"""
    # Primeiro, analisa um texto
    test_text = "Python é uma linguagem de programação incrível"
    client.post("/analyze-text", json={"text": test_text})
    
    # Busca um termo que existe
    response = client.get("/search-term?term=Python")
    assert response.status_code == 200
    
    data = response.json()
    assert data["term"] == "Python"
    assert data["found"] == True
    assert data["occurrences"] >= 1

def test_search_term_not_found():
    """Testa busca de termo que não existe"""
    response = client.get("/search-term?term=inexistente123")
    assert response.status_code == 200
    
    data = response.json()
    assert data["term"] == "inexistente123"
    assert data["found"] == False
    assert data["occurrences"] == 0

def test_search_term_empty():
    """Testa busca com termo vazio"""
    response = client.get("/search-term?term=")
    assert response.status_code == 400

# Testes das funções utilitárias

def test_clean_text():
    """Testa a função de limpeza de texto"""
    text = "Olá, mundo! Como você está? 123..."
    cleaned = clean_text(text)
    
    assert "," not in cleaned
    assert "!" not in cleaned
    assert "?" not in cleaned
    assert "." not in cleaned
    assert "123" in cleaned
    assert cleaned.islower()

def test_get_word_frequencies():
    """Testa a função de frequência de palavras"""
    text = "python python java python javascript java"
    frequencies = get_word_frequencies(text, exclude_stopwords=False)
    
    assert len(frequencies) <= 5
    assert frequencies[0].word == "python"
    assert frequencies[0].frequency == 3
    assert frequencies[1].word == "java"
    assert frequencies[1].frequency == 2

def test_simple_sentiment_analysis():
    """Testa a análise de sentimento simples"""
    # Texto positivo
    positive_text = "Eu amo este projeto fantástico e maravilhoso"
    sentiment = simple_sentiment_analysis(positive_text)
    assert sentiment.sentiment == "positivo"
    assert sentiment.confidence > 0.5
    
    # Texto negativo
    negative_text = "Este projeto é terrível e horrível, odeio tudo"
    sentiment = simple_sentiment_analysis(negative_text)
    assert sentiment.sentiment == "negativo"
    assert sentiment.confidence > 0.5
    
    # Texto neutro
    neutral_text = "O projeto tem algumas funcionalidades implementadas"
    sentiment = simple_sentiment_analysis(neutral_text)
    assert sentiment.sentiment == "neutro"

def test_analyze_multiple_texts():
    """Testa análise de múltiplos textos para verificar cache"""
    texts = [
        "Primeiro texto de exemplo para análise",
        "Segundo texto diferente com outras palavras",
        "Terceiro texto para completar os testes"
    ]
    
    for text in texts:
        response = client.post("/analyze-text", json={"text": text})
        assert response.status_code == 200
    
    # Verifica health para ver se cache aumentou
    response = client.get("/health")
    data = response.json()
    assert data["cache_size"] >= len(texts)

if __name__ == "__main__":
    pytest.main([__file__])
