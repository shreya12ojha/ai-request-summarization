from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(
    title="Request Summarization Orchestrator",
    description="Simulates Azure Logic App locally",
    version="1.0"
)

AZURE_FUNCTION_URL = "http://localhost:7071/api/SummarizeRequest"

@app.post("/process-request")
def process_request(payload: dict):
    #Validate input
    text = payload.get("text")
    if not text or not isinstance(text, str):
        raise HTTPException(
            status_code=400,
            detail="Invalid input: 'text' field is required"
        )

    #Call Azure Function
    try:
        response = requests.post(
            AZURE_FUNCTION_URL,
            json={"text": text},
            timeout=10
        )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=500,
            detail="Failed to reach Azure Function"
        )

    #Handle function errors
    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Azure Function returned an error"
        )

    #Return structured response
    return response.json()
