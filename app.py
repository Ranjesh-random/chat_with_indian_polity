from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# Load environment variables
load_dotenv()

# Load and process text file with explicit UTF-8 encoding
loader = TextLoader("polity_text.txt", encoding='utf-8')
try:
    data = loader.load()
except Exception as e:
    print(f"Error loading file: {e}")
    # You might want to exit here if the file can't be loaded
    import sys
    sys.exit(1)

# Rest of your code remains the same
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                               chunk_overlap = 100)
docs = text_splitter.split_documents(data)

vectorstore = Chroma.from_documents(
    documents=docs, 
    embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
)
retriever = vectorstore.as_retriever(
    search_type="similarity", 
    search_kwargs={"k": 2}
)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=256 ,
    timeout=5
)

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = RunnableParallel({
    "context": retriever,
    "input": RunnablePassthrough()
}) | document_chain

# Get and print response
response = rag_chain.invoke("please tell me about indian prime minister")
print(response)