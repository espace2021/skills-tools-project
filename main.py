from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from langchain_core.runnables.config import RunnableConfig
from langgraph_sdk.runtime import ServerRuntime   # Important pour LangGraph

load_dotenv()

# ==================== VARIABLES GLOBALES ====================
app_state = {}   # Renommé pour éviter la confusion avec le state LangGraph


# ==================== LIFESPAN (Initialisation unique) ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialisation au démarrage
    from graph.workflow import create_graph   # Import ici pour éviter les imports circulaires
    
    graph, cars_tools, emails_tools = await create_graph()
    
    app_state["graph"] = graph
    app_state["cars_tools"] = cars_tools
    app_state["emails_tools"] = emails_tools

    print("✅ Graph and tools loaded successfully at startup")
    
    yield
    
    # Nettoyage à l'arrêt
    app_state.clear()
    print("🧹 App state cleared")


# ==================== FASTAPI APP ====================
app = FastAPI(
    title="Car Marketing AI",
    lifespan=lifespan
)


# ==================== FONCTION COMPATIBLE LANGGRAPH ====================
async def myggraph(runtime: ServerRuntime | None = None, config: RunnableConfig | None = None):
    """
    Fonction compatible avec langgraph.json + LangGraph Platform
    """
    if not app_state:
        raise RuntimeError("Application state not initialized. Is the app running?")

    graph = app_state["graph"]
    cars_tools = app_state["cars_tools"]
    emails_tools = app_state["emails_tools"]

    # Exécution du graphe
    result = await graph.ainvoke({
        "cars_tools": cars_tools,
        "emails_tools": emails_tools,
    }, config=config or RunnableConfig(tags=["api"]))

    return {
        "promotions": result.get("promotions", []),
        "final_emails": result.get("final_emails", []),
    }


# ==================== ENDPOINT FASTAPI ====================
@app.get("/")
async def home():
    return {
        "message": "Car Marketing AI is running with LangGraph",
        "status": "healthy"
    }

@app.post("/run-marketing")
async def run_marketing():
    """Endpoint FastAPI classique"""
    result = await myggraph()   # On appelle la même fonction
    
    return {
        "promotions": result.get("promotions", []),
        "final_emails": result.get("final_emails", [])
    }