import asyncio

from langgraph.graph import StateGraph, END
from graph.state import MarketingState

from skills.clients_skill import get_clients
from skills.marketing_skill import generate_marketing_text

from langchain_mcp_adapters.client import MultiServerMCPClient
from services.gemini_service import ask_gemini_with_tools

import json


# =========================================================
# MCP INIT
# =========================================================

async def build_graph():
    MCP_URL = "http://127.0.0.1:8001/mcp"

    client = MultiServerMCPClient(
        connections={
            "main": {
                "url": MCP_URL,
                "transport": "streamable_http"
            }
        }
    )

    tools = await client.get_tools()


    cars_tools = [t for t in tools if "cars" in t.name or "voitures" in t.name]
    emails_tools = [t for t in tools if "emails" in t.name or "e-mails" in t.name]

    return cars_tools, emails_tools


# =========================================================
# NODES
# =========================================================

import json

def normalize_data(raw):

    print("NORMALIZE RAW =", raw)

    # MCP content list
    if isinstance(raw, list):

        first = raw[0] if raw else {}

        if isinstance(first, dict):

            # FastMCP content text
            if "text" in first:

                raw = first["text"]

    # JSON string
    if isinstance(raw, str):

        try:
            raw = json.loads(raw)

        except Exception as e:
            print("JSON ERROR:", e)
            return []

    # dict -> list
    if isinstance(raw, dict):
        return [raw]

    # already list
    if isinstance(raw, list):
        return raw

    return []

async def load_cars_node(state):

    cars_tools = state.get("cars_tools", [])

    result = []

    for tool in cars_tools:

        if "car" in tool.name:

            result = await tool.ainvoke({})
            break

    return {
        "cars": result
    }


def load_clients_node(state):
    return {
        "clients": get_clients()
    }


def generate_promotions_node(state):

    raw = state.get("cars")

    cars = normalize_data(raw)

    print("CARS =", cars)

    promotions = []

    for car in cars:

        text = generate_marketing_text(car)

        promotions.append({
            "car": car,
            "text": text
        })

    return {
        "promotions": promotions
    }


def generate_emails_node(state):
    final_emails = []
    emails_tools = state.get("emails_tools", [])

    for promo in state["promotions"]:
        email = ask_gemini_with_tools(
            f"""
Tu es un expert marketing automobile.
Créer un email marketing.

CAR: {promo['car']}
PROMO: {promo['text']}
""",
            tools=emails_tools
        )
        final_emails.append({"car": promo["car"], "email": email})

    return {"final_emails": final_emails}

# =========================================================
# GRAPH FACTORY
# =========================================================

async def create_graph():
    cars_tools, emails_tools = await build_graph()

    workflow = StateGraph(MarketingState)

    workflow.add_node("load_cars", load_cars_node)
    workflow.add_node("load_clients", load_clients_node)
    workflow.add_node("generate_promotions", generate_promotions_node)
    workflow.add_node("generate_emails", generate_emails_node)

    workflow.set_entry_point("load_cars")

    workflow.add_edge("load_cars", "load_clients")
    workflow.add_edge("load_clients", "generate_promotions")
    workflow.add_edge("generate_promotions", "generate_emails")
    workflow.add_edge("generate_emails", END)

    graph = workflow.compile()
    
    return graph,cars_tools, emails_tools

# =========================================================
# RUN
# =========================================================


#graph,cars_tools, emails_tools = asyncio.run(create_graph())