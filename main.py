from typing import List
from time import sleep
import getpass
import os

from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv

from search_engine import SearchEngine


MAX_HISTORY = 3

load_dotenv()

if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = getpass.getpass('Gemini api key: ')

search_engine = SearchEngine()
model = ChatGoogleGenerativeAI(model='gemini-1.5-pro')
vector_store = InMemoryVectorStore(embedding=GoogleGenerativeAIEmbeddings(model='models/text-embedding-004'))
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

documents: List[Document] = []


def get_documents():
    print('Digite os termos de busca para adicionar documentos. Digite "continue" para prosseguir.', end='\n\n')
    
    while True:
        term = input('documento: ').strip()

        if term.lower() == 'continue':
            break

        content = search_engine.search(term)

        if not content:
            print('Conteúdo não encontrado! Tente outro termo.')
            continue

        temp_doc = Document(page_content=content)

        chunks = text_splitter.split_documents([temp_doc])
        for chunk in chunks:
            chunk.metadata.update({
                'source': term,
                'chunk_id': len(documents) + 1
            })

        documents.extend(chunks)
        print(f'Documento adicionado! Total de chunks: {len(documents)}')


get_documents()
vector_store.add_documents(documents=documents)

retriever = vector_store.as_retriever(search_kwargs={'k': 5, 'score_threshold': 0.7})

system_prompt = '''
Você é uma assistente especialista. Siga estas regras:
1. Use o contexto primeiro
2. Se precisar calcular, explique o passo a passo
3. Se faltar informação, use conhecimento geral válido até 2023

Contexto: {context}
'''

question_history: List[HumanMessage] = []


def chat():
    question = input('?>> ')
    docs = retriever.invoke(question)
    docs_text = "".join(d.page_content for d in docs)
    system_prompt_fmt = system_prompt.format(context=docs_text)

    question_history.append(HumanMessage(content=question))

    if len(question_history) > MAX_HISTORY:
        question_history.pop(0)

    response = model.invoke([SystemMessage(content=system_prompt_fmt), *question_history])

    print(response.content)


while True:
    try:
        chat()
    except ResourceExhausted:
        sleep(20)
        chat()
    except KeyboardInterrupt:
        print('exiting...')
        exit(0)
