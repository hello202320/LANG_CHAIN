from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
import datetime

def log_text(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {text}\n\n"
    with open("log_file.txt", "a") as file:
        file.write(log_entry)

def main():
    load_dotenv()
    st.set_page_config(page_title="LANG_CHAIN")
    st.header("PDF Q&A📚")

    pdf = st.file_uploader("Upload PDF 👇:", type="pdf")
    pdf_text = None
    
    if pdf is not None:
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
        text += page.extract_text()
      pdf_text = text
      
      text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
      )
      chunks = text_splitter.split_text(text)
    
      embeddings = OpenAIEmbeddings()
      knowledge_base = FAISS.from_texts(chunks, embeddings)
      
      user_question = st.text_input("Enter your PDF question: ")
      if user_question:
        docs = knowledge_base.similarity_search(user_question)
        
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")#change the model https://platform.openai.com/account/rate-limits
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
          response = chain.run(input_documents=docs, question=user_question)
          log_text(str(cb)) #log costs
           
        st.write(response)
      st.write(pdf_text) #display pdf
if __name__ == '__main__':
    main()