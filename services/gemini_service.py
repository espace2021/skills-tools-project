from dotenv import load_dotenv
import os

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


def ask_gemini(prompt: str):

    response = llm.invoke(prompt)

    return response.content

def ask_gemini_with_tools(prompt: str, tools: list):

    response = llm.invoke(
        prompt,
        tools=tools
    )

    return response.content

def create_gemini_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )