from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Langchain server",
    version="1.0",
    description="A simple API Server"
)

llm = ChatGoogleGenerativeAI(temperature=0.8, model="gemini-2.0-flash")
outout_parser = StrOutputParser()

prompt1 = ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")

add_routes(
    app,
    prompt1 | llm | outout_parser,
    path="/essay"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:*", "*"],  # Permissive for local dev
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "*"],  # Explicitly include OPTIONS
    allow_headers=["Content-Type", "Authorization", "Accept", "*"],  # Cover common headers
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)