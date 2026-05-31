import json
from fastmcp import FastMCP

from services.sheets_service import (
    get_sheet_records
)


# ====================== MCP TOOLS ======================

def register_tools(mcp: FastMCP):

    @mcp.tool
    async def get_cars() -> str:
        try:
            data = get_sheet_records("voitures") # nom du sheet
      
            return json.dumps(data, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)

# ====================== AFFICHAGE DES TOOLS ======================

    tools = [
        "get_cars"
    ]

    print("\n📌 Tools enregistrés de conference :")
    for tool_name in tools:
        print(f" • {tool_name}")