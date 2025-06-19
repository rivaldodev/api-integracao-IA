# Instruções para Configuração da API Key do Google Gemini

## Passo a Passo

### 1. Obter a API Key
1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a API key gerada

### 2. Configurar no Projeto
1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edite o arquivo `.env` e substitua `your_gemini_api_key_here` pela sua API key:
   ```
   GEMINI_API_KEY=sua_api_key_real_aqui
   ```

### 3. Reiniciar a API
Após configurar a API key, reinicie a aplicação para que as alterações tenham efeito.

## Análise de Sentimento

Com a API key configurada:
- ✅ Análise de sentimento usando Google Gemini 2.0 Flash
- ✅ Detecção precisa de emoções e tons
- ✅ Explicações detalhadas dos resultados

Sem a API key:
- ⚠️ Análise de sentimento básica usando palavras-chave
- ⚠️ Resultados limitados mas funcionais
- ⚠️ Confiança reduzida nas análises

## Notas Importantes
- A API funciona perfeitamente sem a chave do Gemini
- A análise de sentimento será limitada mas ainda útil
- Todos os outros recursos permanecem totalmente funcionais
