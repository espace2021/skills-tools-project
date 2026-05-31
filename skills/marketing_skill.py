from skills.prompt_loader import load_prompt
from services.gemini_service import ask_gemini

marketing_prompt = load_prompt("marketing")


def generate_marketing_text(car):

    marque = car.get("marque", "Inconnue")
    modele = car.get("modele", "Inconnu")
    prix = car.get("prix", "Non spécifié")
    carburant = car.get("carburant", "Non spécifié")

    final_prompt = f"""
{marketing_prompt}

DONNÉES VOITURE :

Marque : {marque}
Modèle : {modele}
Prix : {prix}
Carburant : {carburant}
"""

    return ask_gemini(final_prompt)