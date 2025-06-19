"""
🚀 DEMONSTRAÇÃO FINAL - API de Análise de Texto com Gemini 2.0 Flash
=======================================================================

Este script demonstra todas as funcionalidades da API desenvolvida para a seleção.
"""

import requests
import json
import time
from datetime import datetime

def print_header(title):
    """Imprime um cabeçalho bonito"""
    print(f"\n{'='*70}")
    print(f"🎯 {title}")
    print(f"{'='*70}")

def print_section(title):
    """Imprime uma seção"""
    print(f"\n{'─'*50}")
    print(f"📋 {title}")
    print(f"{'─'*50}")

def test_api():
    """Testa se a API está funcionando"""    try:
        response = requests.get("http://localhost:3000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API está funcionando!")
            print(f"   🔹 Status: {data['status']}")
            print(f"   🔹 Gemini 2.0 Flash: {'✅ Configurado' if data['gemini_configured'] else '❌ Não configurado'}")
            print(f"   🔹 Análises em cache: {data['cache_size']}")
            return True
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar com a API: {e}")
        print("   💡 Certifique-se de que a API está rodando em: http://localhost:3000")
        return False

def analyze_text(text, description=""):
    """Analisa um texto"""
    print(f"\n🔍 Analisando: {description}")
    print(f"📝 Texto: \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
    
    try:        response = requests.post(
            "http://localhost:3000/analyze-text",
            json={"text": text},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Análise concluída!")
            print(f"   📊 Palavras: {data['word_count']}")
            
            print(f"   🔤 Top 5 palavras:")
            for i, word in enumerate(data['most_frequent_words'], 1):
                print(f"      {i}. {word['word']} ({word['frequency']}x)")
            
            sentiment = data['sentiment_analysis']
            emoji = {"positivo": "😊", "negativo": "😞", "neutro": "😐"}
            print(f"   {emoji.get(sentiment['sentiment'], '🤔')} Sentimento: {sentiment['sentiment']}")
            print(f"   🎯 Confiança: {sentiment['confidence']:.1%}")
            print(f"   💭 Explicação: {sentiment['explanation']}")
            
            return data
        else:
            print(f"❌ Erro na análise: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def search_term(term):
    """Busca um termo"""
    try:
        response = requests.get(f"http://localhost:3000/search-term?term={term}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data['found']:
                print(f"✅ '{term}' encontrado!")
                print(f"   📈 Ocorrências: {data['occurrences']}")
                if data.get('last_analysis_timestamp'):
                    print(f"   ⏰ Última análise: {data['last_analysis_timestamp']}")
            else:
                print(f"❌ '{term}' não encontrado nas análises")
            
            return data
        else:
            print(f"❌ Erro na busca: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def main():
    """Função principal"""
    print_header("DEMONSTRAÇÃO COMPLETA DA API")
    print(f"🕐 Iniciado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    print("👨‍💻 Desenvolvido por: Rivaldo Freitas de Carvalho")
    print("🎯 Challenge by: Coodesh")
    
    # Testa conexão
    if not test_api():
        return
    
    print_section("1. ANÁLISES DE SENTIMENTO COM GEMINI 2.0 FLASH")
    
    # Exemplos de textos
    exemplos = [
        {
            "texto": "Este projeto de API está absolutamente fantástico! A integração com Gemini 2.0 Flash funcionou perfeitamente e estou muito satisfeito com os resultados incríveis.",
            "desc": "Texto muito positivo"
        },
        {
            "texto": "Infelizmente este código está cheio de bugs terríveis e problemas frustrantes. Não consigo fazer funcionar de jeito nenhum, que situação horrível!",
            "desc": "Texto muito negativo"
        },
        {
            "texto": "A API foi desenvolvida usando FastAPI e Python. Implementa endpoints para análise de texto e integração com Google Gemini para processamento de linguagem natural.",
            "desc": "Texto técnico neutro"
        },
        {
            "texto": "Python é uma linguagem de programação versátil. FastAPI oferece alta performance para APIs REST. Google Gemini 2.0 Flash proporciona análises avançadas de IA.",
            "desc": "Texto informativo"
        }
    ]
    
    for i, exemplo in enumerate(exemplos, 1):
        analyze_text(exemplo["texto"], f"{i}/4 - {exemplo['desc']}")
        time.sleep(1)  # Pausa para não sobrecarregar a API
    
    print_section("2. DEMONSTRAÇÃO DE BUSCA DE TERMOS")
    
    termos = ["Python", "fantástico", "API", "problemas", "Gemini", "inexistente"]
    
    for termo in termos:
        print(f"\n🔍 Buscando: '{termo}'")
        search_term(termo)
    
    print_section("3. ESTATÍSTICAS FINAIS")
    
    # Verifica status final
    try:
        response = requests.get("http://localhost:3000/health")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total de análises realizadas: {data['cache_size']}")
            print(f"🕐 Timestamp final: {data['timestamp']}")
    except:
        pass
    
    print_header("DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO! 🎉")
    print("✨ Principais funcionalidades demonstradas:")
    print("   🔹 Análise de texto com contagem de palavras")
    print("   🔹 Identificação das 5 palavras mais frequentes")
    print("   🔹 Análise de sentimento com Google Gemini 2.0 Flash")
    print("   🔹 Sistema de cache para histórico")
    print("   🔹 Busca de termos em análises anteriores")
    print("   🔹 API RESTful com FastAPI")
    print("   🔹 Documentação automática com Swagger")
    print("   🔹 Tratamento robusto de erros")    print("\n📖 Acesse a documentação: http://localhost:3000/docs")
    print("🌐 API Base URL: http://localhost:3000")

if __name__ == "__main__":
    main()
