from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import PromptTemplate
from backend.config import settings
from backend.rag.retriever import get_retriever

CUSTOM_PROMPT = """You are a helpful Banking Support Assistant. Use the following retrieved context to answer the user's question. If you don't know the answer, say so clearly. Be concise and professional.

Retrieved Context:
{context}

Chat History:
{chat_history}

Current Question: {question}

Answer:"""

PROMPT = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template=CUSTOM_PROMPT
)

def get_session_history(session_id: str):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chat_memory.db"
    )

def get_chat_chain():
    retriever = get_retriever()
    if not retriever:
        return None
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=settings.OPENAI_API_KEY,
        temperature=0.2
    )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": PROMPT},
        return_source_documents=True,
        verbose=False
    )
    
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )