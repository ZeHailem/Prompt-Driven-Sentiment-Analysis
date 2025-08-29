import re
def clean_llm_response(text: str) -> str:
    """
    Remove ```json ... ``` fences and extra whitespace from LLM output
    """
    # Remove ```json or ``` at start and ``` at end
    cleaned = re.sub(r"^```json\s*", "", text)
    cleaned = re.sub(r"^```", "", cleaned)
    cleaned = re.sub(r"```$", "", cleaned)
    return cleaned.strip()
