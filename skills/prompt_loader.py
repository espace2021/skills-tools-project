from pathlib import Path

PROMPTS_DIR = Path("skills/prompts")


def load_prompt(prompt_name: str) -> str:

    file_path = PROMPTS_DIR / f"{prompt_name}.md"

    return file_path.read_text(
        encoding="utf-8"
    )