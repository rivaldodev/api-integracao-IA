#!/usr/bin/env python3
"""
Demonstração offline das funcionalidades principais da API
Este script demonstra as funções de análise sem necessidade de servidor
"""

from main import (
    clean_text, 
    get_word_frequencies, 
    simple_sentiment_analysis,
    WordFrequency,
    SentimentAnalysis
)
from datetime import datetime
import json

def demonstrar_funcionalidades():
    """Demonstra as funcionalidades principais da API"""
    
    print("🚀 Demonstração Offline - API de Análise de Texto")
    print("=" * 60)
    print("Desenvolvido por: Rivaldo Freitas de Carvalho")
    print("Challenge by: Coodesh")
    print("=" * 60)
    
    # Textos de exemplo
    textos_exemplo = [
        "Este é um projeto incrível desenvolvido com FastAPI! Estou muito feliz com o resultado e espero que seja aprovado na seleção.",
        "Python é uma linguagem de programação fantástica para desenvolvimento de APIs. FastAPI torna tudo muito mais simples e eficiente.",
        "Infelizmente este projeto não está funcionando como esperado. Há muitos problemas e bugs que precisam ser resolvidos urgentemente.",
        "A integração com Google Gemini AI permite análises de sentimento muito mais precisas e detalhadas do que métodos tradicionais."
    ]
    
    print(f"\n📊 Analisando {len(textos_exemplo)} textos de exemplo...\n")
    
    for i, texto in enumerate(textos_exemplo, 1):
        print(f"{'─' * 60}")
        print(f"📄 Exemplo {i}/{len(textos_exemplo)}")
        print(f"📝 Texto: \"{texto[:50]}{'...' if len(texto) > 50 else ''}\"")
        print()
        
        # Análise de texto
        texto_limpo = clean_text(texto)
        palavras = texto_limpo.split()
        word_count = len(palavras)
        
        # Palavras mais frequentes
        palavras_frequentes = get_word_frequencies(texto)
        
        # Análise de sentimento
        sentimento = simple_sentiment_analysis(texto)
        
        # Resultado
        resultado = {
            "word_count": word_count,
            "most_frequent_words": [
                {"word": wf.word, "frequency": wf.frequency} 
                for wf in palavras_frequentes
            ],
            "sentiment_analysis": {
                "sentiment": sentimento.sentiment,
                "confidence": sentimento.confidence,
                "explanation": sentimento.explanation
            },
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        print("✅ Análise concluída!")
        print(f"   📊 Total de palavras: {resultado['word_count']}")
        print("   🔤 Palavras mais frequentes:")
        for j, word_freq in enumerate(resultado['most_frequent_words'], 1):
            print(f"      {j}. {word_freq['word']} ({word_freq['frequency']}x)")
        
        sentiment_data = resultado['sentiment_analysis']
        print(f"   😊 Sentimento: {sentiment_data['sentiment']}")
        print(f"   🎯 Confiança: {sentiment_data['confidence']:.2f}")
        print(f"   💭 Explicação: {sentiment_data['explanation']}")
        print(f"   ⏰ Timestamp: {resultado['analysis_timestamp']}")
        print()
    
    print("=" * 60)
    print("✨ Demonstração das funcionalidades principais concluída!")
    print()
    print("🔧 Funcionalidades implementadas:")
    print("   ✅ Contagem de palavras")
    print("   ✅ Análise de frequência (sem stopwords)")
    print("   ✅ Análise de sentimento (local + Gemini)")
    print("   ✅ Sistema de cache em memória")
    print("   ✅ Busca de termos em histórico")
    print("   ✅ API REST completa com FastAPI")
    print("   ✅ Documentação automática (Swagger)")
    print("   ✅ Tratamento de erros robusto")
    print("   ✅ Testes automatizados")
    print("   ✅ Logging e monitoramento")
    print()
    print("🌐 Para usar a API completa:")
    print("   1. Execute: python -m uvicorn main:app --host 0.0.0.0 --port 3000")
    print("   2. Acesse: http://localhost:3000/docs")
    print("   3. Configure a API key do Gemini (opcional)")
    print()
    print("📋 Requisitos atendidos:")
    print("   ✅ POST /analyze-text - Análise completa de texto")
    print("   ✅ GET /search-term - Busca de termos")
    print("   ✅ Integração com IA (Google Gemini)")
    print("   ✅ Estatísticas de texto")
    print("   ✅ Sistema de cache/histórico")
    print("   ✅ Tratamento de erros")
    print("   ✅ Documentação completa")
    print("   ✅ Códigos HTTP adequados")
    print("   ✅ Organização profissional do código")

if __name__ == "__main__":
    demonstrar_funcionalidades()
