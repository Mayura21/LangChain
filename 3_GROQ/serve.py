from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

system_template = "Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", "{text}")
    ]
)

parser = StrOutputParser()

# Create chain
chain = prompt | model | parser

# App definition

app = FastAPI(title="Langchain Server",
              version="1.0",
              description="A simple API server using Langchain runnable interfaces")

add_routes(
    app,
    chain,
    path="/chain"
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
