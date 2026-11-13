

import requests

def ask_local_ai(question, context=""):

    prompt = f"""
You are an AI Groundwater Information Assistant.

Use the provided groundwater report information
to answer the user's question.

If information is missing, say it is not available.

Context:
{context}

Question:
{question}

Answer:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        response.raise_for_status()

        return response.json()["response"]

    except Exception as e:
        return f"Error: {e}"

