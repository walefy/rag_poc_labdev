# RAG Python com LangChain e Gemini

Implementação de Retrieval-Augmented Generation (RAG) utilizando:

- Google Gemini como LLM
- Wikipedia como fonte de conhecimento
- LangChain para orquestração
- UV para gestão de dependências

## Pré-requisitos

- Python >=3.13.1
- [UV](https://docs.astral.sh/uv/getting-started/installation/) instalado
- Chave de API do Gemini ([obter aqui](https://aistudio.google.com/apikey))

## Configuração Inicial

1. Clone o repositório:

```bash
git clone git@github.com:walefy/rag_poc_labdev.git
```

2. Instale as dependências

```bash
uv sync
```

3. Configure a API Key:

```bash
cp .env.example .env
# Adicione sua chave no arquivo .env
```

## Executando o projeto

```bash
uv run main.py
```

## Fluxo de Uso

1. Adição de Documentos:
    - Insira termos de busca da Wikipedia
    - Digite continue quando terminar

2. Interface de Chat:
    - Faça perguntas quando aparecer ?>>
    - Ctrl+C para sair

## Exemplo

```text
documento: inteligência artificial
documento: machine learning
documento: continue
?>> explique o que é deep learning
```

## Funcionalidades Principais

- [X] Busca semântica em documentos
- [X] Chunking inteligente de textos
- [X] Histórico de conversação (últimas 3 perguntas)
- [X] Fallback para perguntas fora do contexto

## Limitações Conhecidas

- Taxa limite de requisições da API Gemini
- Qualidade dependente do conteúdo da Wikipedia em português
- Ainda não persiste dados entre execuções
