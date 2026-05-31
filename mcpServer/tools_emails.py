import json
from fastmcp import FastMCP
from langchain_core.documents import Document
from langchain_core.tools import Tool

from services.gemini_service import (
    ask_gemini
)

from services.sheets_service import (
    get_sheet_records       )



    # =========================================================
    # TOOL 
    # =========================================================
def register_tools(mcp: FastMCP):
    @mcp.tool
    async def generate_email(client: str, promotions: str) -> str:
        """
        Écrire des promotions et les envoyer aux clients.
        """
        try:                                         
            records = get_sheet_records("clients")

            client = client if client else "Aucun client spécifié"
            promotions = promotions if promotions else "Aucune promotion spécifiée"

            final_prompt = f"""
            Tu es un spécialiste emailing.

            OBJECTIFS :
            - écrire un email professionnel
            - donner envie d'acheter
            - rester naturel
            - éviter le spam marketing

            STYLE :
            - chaleureux
            - professionnel
            - moderne

            CLIENT :
            {client}

            PROMOTIONS :
            {promotions}

            Génère un email complet.
            """

            result = ask_gemini(final_prompt)

            # ✅ Return a plain string, not a nested object
            if isinstance(result, str):
                return result
            elif isinstance(result, dict):
                return result.get("text") or result.get("content") or json.dumps(result, ensure_ascii=False)
            else:
                return str(result)

        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)

    # =========================================================
    # AFFICHAGE DES TOOLS
    # =========================================================
tools = [
        "generate_email" 
    ]

print("\n📌 Tools enregistrés :")
for tool_name in tools:
    print(f" • {tool_name}")