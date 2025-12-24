# AI-Based Request Summarisation Workflow (Azure + OpenAI)

## Overview
This project implements an AI-powered serverless workflow that automatically summarises and categorises free-text requests. It is designed to reduce manual triage effort by converting unstructured user requests into structured, actionable information.

The solution follows a cloud-native architecture using:
- An orchestration layer (simulated locally)
- Azure Functions for processing
- OpenAI for summarisation and classification

---

## Problem Statement
IT and support teams often receive a large number of free-text requests through emails or forms. These requests must be manually read, summarised, categorised, and forwarded to the appropriate team, making the process slow and error-prone.

This project automates that workflow using AI.

---

## Architecture Overview
```txt
Client (HTTP Request)
│
└── HTTP Orchestration Layer
    (Local simulation of Azure Logic App)
        │
        └── Azure Function (Python)
                │
                └── OpenAI API
                        │
                        └── Summary + Category (JSON Response)
```


### Architecture Explanation
- The orchestration layer manages the request flow and acts as the trigger.
- The Azure Function handles AI-related processing.
- OpenAI generates a concise summary and categorises the request.
- The final structured response is returned as JSON.

---

## Workflow
1. A free-text request is sent via HTTP.
2. The orchestration layer receives and validates the request.
3. The request text is forwarded to the Azure Function.
4. The Azure Function sends the text to OpenAI.
5. OpenAI returns a summary and category.
6. The response is returned to the caller in JSON format.

---

## Technology Stack
- Python
- Azure Functions (local runtime)
- OpenAI API
- FastAPI (local orchestration layer)
- HTTP-based communication

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Azure Functions Core Tools
- OpenAI API Key

### Environment Configuration
Set the OpenAI API key using environment variables:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Run Azure Function Locally
```bash
func start
```

The function will be available at: http://localhost:7071/api/SummarizeRequest

Run Orchestration Layer
```bash
uvicorn logic_app_simulator:app --reload --port 8000
```
## Sample Request/Response

Sample Request
```bash
{
  "text": "Hi team, I’ve just joined the finance department and can’t access the reporting dashboard or the finance SharePoint folders."
}
```

Sample Response
```bash
{
  "summary": "New finance employee requesting access to the reporting dashboard and finance SharePoint folders.",
  "category": "Access Request"
}
```