import json
import os
import logging
import azure.functions as func
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = func.FunctionApp()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route(route="SummarizeRequest", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def summarize_request(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("AI request summarization started")

    try:
        body = req.get_json()
        text = body.get("text")

        if not text:
            return func.HttpResponse(
                json.dumps({"error": "Text input is required"}),
                status_code=400,
                mimetype="application/json"
            )

        prompt = f"""
Summarize the following IT request in one sentence and classify it.

Allowed categories:
- Access Request
- Incident
- General Query
- Other

Request:
{text}

Respond ONLY in valid JSON:
{{"summary": "...", "category": "..."}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        result = response.choices[0].message.content

        return func.HttpResponse(
            result,
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )
