from fastapi import FastAPI
from pathlib import Path
import openai
import json
import os
import Clean

api_key = os.getenv("OPENAI_API_KEY")  # Get API key from environment variable

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=api_key)

app = FastAPI(title="User Feedback API")


@app.post("/analyze-feedback-file")
async def analyze_feedback_file():
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "Data" / "feedback.txt"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            feedback_list = f.read().splitlines()
    except Exception as e:
        return {"error": str(e), "path_checked": str(file_path)}

    results = []

    for feedback in feedback_list:
        if feedback.strip():
            prompt = f"""
            Analyze the following feedback and return response in JSON format with:
            - product_type
            - brand
            - feedback_category (positive or negative)
            - original_feedback
            Feedback: "{feedback.strip()}"
            """
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes user feedback. If the feedback is incomplete and does not contain product type or brand, return None for them. Always include the original feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            response_text = response.choices[0].message.content
            clean_text = Clean.clean_llm_response(response_text)

            try:
                structured = json.loads(clean_text)
            except json.JSONDecodeError:
                structured = {"raw": clean_text}

            results.append(structured)

    return {"results": results}
