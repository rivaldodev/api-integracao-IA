"""
Exemplo de uso da API de Análise de Texto
Este arquivo demonstra como usar a API através de código Python
"""

import requests
import json
from datetime import datetime

# URL base da API
BASE_URL = "http://localhost:3000"

def test_api_connection():
    """Testa se a API está funcionando"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API está funcionando!")
            data = response.json()
            print(f"   Status: {data['status']}")
            print(f"   Gemini configurado: {data['gemini_configured']}")
            print(f"   Análises em cache: {data['cache_size']}")
            return True
        else:
            print("❌ API não está respondendo corretamente")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com a API: {e}")
        print("   Certifique-se de que a API está rodando em http://localhost:3000")
        return False

def analyze_text_example(text):
    """Exemplo de análise de texto"""
    print(f"\n📝 Analisando texto: \"{text[:50]}{'...' if len(text) > 50 else ''}\"")
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze-text",
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Análise concluída!")
            print(f"   📊 Total de palavras: {data['word_count']}")
            print("   🔤 Palavras mais frequentes:")
            for i, word_freq in enumerate(data['most_frequent_words'], 1):
                print(f"      {i}. {word_freq['word']} ({word_freq['frequency']}x)")
            
            sentiment = data['sentiment_analysis']
            print(f"   😊 Sentimento: {sentiment['sentiment']}")
            print(f"   🎯 Confiança: {sentiment['confidence']:.2f}")
            if sentiment.get('explanation'):
                print(f"   💭 Explicação: {sentiment['explanation']}")
            
            print(f"   ⏰ Timestamp: {data['analysis_timestamp']}")
            
            return data
        else:
            print(f"❌ Erro na análise: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao analisar texto: {e}")
        return None

def search_term_example(term):
    """Exemplo de busca de termo"""
    print(f"\n🔍 Buscando termo: \"{term}\"")
    
    try:
        response = requests.get(f"{BASE_URL}/search-term?term={term}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data['found']:
                print(f"✅ Termo encontrado!")
                print(f"   📈 Ocorrências: {data['occurrences']}")
                if data.get('last_analysis_timestamp'):
                    print(f"   ⏰ Última análise: {data['last_analysis_timestamp']}")
            else:
                print("❌ Termo não encontrado nas análises anteriores")
            
            return data
        else:
            print(f"❌ Erro na busca: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao buscar termo: {e}")
        return None

def main():
    """Função principal com exemplos"""
    print("🚀 Demonstração da API de Análise de Texto")
    print("=" * 60)
    
    # Testa conexão
    if not test_api_connection():
        return
    
    # Exemplos de textos para análise
    textos_exemplo = [
        "Este é um projeto incrível desenvolvido com FastAPI! Estou muito feliz com o resultado e espero que seja aprovado na seleção.",
        
        "Python é uma linguagem de programação fantástica para desenvolvimento de APIs. FastAPI torna tudo muito mais simples e eficiente.",
        
        "Infelizmente este projeto não está funcionando como esperado. Há muitos problemas e bugs que precisam ser resolvidos urgentemente.",
        
        "A integração com Google Gemini AI permite análises de sentimento muito mais precisas e detalhadas do que métodos tradicionais.",
        
        "API REST endpoints JSON HTTP POST GET análise texto sentimento palavras frequência estatísticas dados processamento linguagem natural"
    ]
    
    # Analisa cada texto
    print(f"\n📋 Analisando {len(textos_exemplo)} textos de exemplo...")
    
    for i, texto in enumerate(textos_exemplo, 1):
        print(f"\n{'─' * 60}")
        print(f"📄 Exemplo {i}/{len(textos_exemplo)}")
        analyze_text_example(texto)
    
    # Exemplos de busca
    print(f"\n{'=' * 60}")
    print("🔍 Exemplos de busca de termos:")
    
    termos_busca = ["projeto", "Python", "API", "incrível", "problema", "inexistente"]
    
    for termo in termos_busca:
        search_term_example(termo)
    
    # Informações finais
    print(f"\n{'=' * 60}")
    print("✨ Demonstração concluída!")
    print("\n📖 Para mais informações:")
    print(f"   • Documentação Swagger: {BASE_URL}/docs")
    print(f"   • API Info: {BASE_URL}/")
    print(f"   • Health Check: {BASE_URL}/health")

if __name__ == "__main__":
    main()
