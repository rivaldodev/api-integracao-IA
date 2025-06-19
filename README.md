# API de Análise de Texto

Uma API RESTful moderna para análise de texto que oferece estatísticas detalhadas e análise de sentimento utilizando Google Gemini AI.

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**
- **FastAPI** - Framework web moderno e de alta performance
- **Google Gemini 2.0 Flash** - Para análise avançada de sentimento
- **Uvicorn** - Servidor ASGI de alta performance
- **Pydantic** - Validação de dados e serialização

## 📋 Funcionalidades

### ✅ Requisitos Obrigatórios

- **POST /analyze-text**: Analisa textos e retorna:
  - Contagem total de palavras
  - 5 palavras mais frequentes (excluindo stopwords)
  - Análise de sentimento usando Google Gemini 2.0 Flash (gemini-2.0-flash)

### ✅ Funcionalidades Opcionais

- **GET /search-term**: Busca termos em análises anteriores
- **GET /health**: Verificação de saúde da API
- **GET /**: Informações gerais da API
- Sistema de cache em memória para histórico de análises
- Documentação automática com Swagger UI

## 🛠️ Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/rivaldodev/api-integracao-IA
cd integracao_ia
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a API Key do Google Gemini
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua API key
GEMINI_API_KEY=sua_api_key_aqui
```

Para obter uma API key do Google Gemini:
1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Crie uma nova API key
4. Copie e cole no arquivo `.env`

### 4. Execute a aplicação

#### Opção 1: Usando o script run.py (Recomendado)
```bash
python run.py
```

#### Opção 2: Diretamente com uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

A API estará disponível em:
- **Aplicação**: http://localhost:3000
- **Documentação Swagger**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

## 📡 Endpoints da API

### POST /analyze-text

Analisa um texto fornecido e retorna estatísticas e sentimento.

**Request Body:**
```json
{
  "text": "Seu texto livre aqui..."
}
```

**Response:**
```json
{
  "word_count": 10,
  "most_frequent_words": [
    {"word": "exemplo", "frequency": 3},
    {"word": "texto", "frequency": 2}
  ],
  "sentiment_analysis": {
    "sentiment": "positivo",
    "confidence": 0.85,
    "explanation": "Texto apresenta tom otimista e palavras positivas"
  },
  "analysis_timestamp": "2024-01-15T10:30:00"
}
```

### GET /search-term?term=palavra

Busca um termo específico nas análises anteriores.

**Response:**
```json
{
  "term": "palavra",
  "found": true,
  "occurrences": 5,
  "last_analysis_timestamp": "2024-01-15T10:30:00"
}
```

### GET /health

Verifica o status da API e configurações.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "gemini_configured": true,
  "cache_size": 10
}
```

## 🧪 Exemplos de Uso

### Usando curl

```bash
# Analisar texto
curl -X POST "http://localhost:3000/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Este é um projeto incrível e muito bem desenvolvido!"}'

# Buscar termo
curl "http://localhost:3000/search-term?term=projeto"

# Verificar saúde
curl "http://localhost:3000/health"
```

### Usando Python requests

```python
import requests

# Analisar texto
response = requests.post(
    "http://localhost:3000/analyze-text",
    json={"text": "Este é um projeto incrível e muito bem desenvolvido!"}
)
print(response.json())

# Buscar termo
response = requests.get("http://localhost:3000/search-term?term=projeto")
print(response.json())
```

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `GEMINI_API_KEY` | API Key do Google Gemini | - |
| `APP_HOST` | Host da aplicação | 0.0.0.0 |
| `APP_PORT` | Porta da aplicação | 8000 |
| `APP_DEBUG` | Modo debug | False |
| `LOG_LEVEL` | Nível de log | INFO |

### Stopwords

A API automaticamente remove palavras comuns em português (stopwords) da análise de frequência, incluindo:
- Artigos: a, o, um, uma
- Preposições: de, em, para, com
- Pronomes: ele, ela, isso, você
- E outras palavras comuns

## 🏗️ Arquitetura

```
integracao_ia/
├── main.py              # Aplicação principal FastAPI
├── run.py               # Script de inicialização
├── requirements.txt     # Dependências Python
├── .env.example        # Exemplo de configuração
├── .gitignore          # Arquivos ignorados pelo Git
└── README.md           # Este arquivo
```

## 🔍 Tratamento de Erros

A API implementa tratamento robusto de erros:

- **400 Bad Request**: Texto vazio ou dados inválidos
- **500 Internal Server Error**: Erros internos do servidor
- **Fallback**: Se o Gemini não estiver disponível, usa análise local de sentimento

## 📊 Monitoramento

- Logging detalhado de todas as operações
- Cache em memória para otimização de performance
- Endpoint de health check para monitoramento
- Timestamps em todas as análises

## 🚀 Deploy em Produção

Para deploy em produção, considere:

1. **Usar variáveis de ambiente** para configuração
2. **Configurar HTTPS** para segurança
3. **Implementar rate limiting** para controle de uso
4. **Usar banco de dados** em vez de cache em memória
5. **Configurar logs estruturados** para monitoramento

## 🤝 Contribuições

Este projeto foi desenvolvido como parte de um desafio técnico. Para melhorias futuras, considere:

- Adicionar autenticação e autorização
- Implementar persistência em banco de dados
- Adicionar mais idiomas de análise
- Implementar análise de emoções específicas
- Adicionar métricas de performance

---

**This is a challenge by [Coodesh](https://coodesh.com/)**

Desenvolvido por **[Rivaldo Freitas de Carvalho](https://github.com/rivaldodev)**

