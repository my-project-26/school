import json
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Schul-App Backend")

# CORS-Freigabe für Safari & Chrome (Frontend Live Server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2" # Oder mistral / phi3

class TaskRequest(BaseModel):
    topic: str # z.B. "1x1", "Textaufgabe", "Anlaut"
    grade: int # 1 oder 3

@app.get("/")
def read_root():
    return {"status": "Schul-App Backend läuft!"}

@app.post("/api/generate-task")
def generate_task(req: TaskRequest):
    if req.grade == 3 and req.topic == "Textaufgabe":
        prompt = (
            "Du bist ein Grundschullehrer für die 3. Klasse in Deutschland. "
            "Erstelle eine kurze, einfache Mathe-Textaufgabe zum Thema Multiplikation/Einmaleins im Zahlenraum bis 100. "
            "Antworte AUSSCHLIESSLICH im folgenden JSON-Format ohne weiteren Text:\n"
            "{\n"
            '  "text": "Fragetext der Aufgabe",\n'
            '  "num1": 6,\n'
            '  "num2": 7,\n'
            '  "answer": 42,\n'
            '  "hint": "Rechenweg-Hilfe (z.B. 6 * 7)"\n'
            "}"
        )
    else:
        raise HTTPException(status_code=400, detail="Thema/Klasse nicht unterstützt")

    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=10)
        response_json = response.json()
        
        # Output parsen
        raw_text = response_json.get("response", "")
        clean_json = raw_text[raw_text.find('{'):raw_text.rfind('}')+1]
        data = json.loads(clean_json)
        return data

    except Exception as e:
        # Fallback falls Ollama nicht erreichbar ist (Offline-Safety)
        print(f"Ollama nicht erreichbar ({e}), nutze Fallback-Aufgabe.")
        return {
            "text": "In einer Bäckerei stehen 4 Bleche mit jeweils 8 Brezeln. Wie viele Brezeln sind es insgesamt?",
            "num1": 4,
            "num2": 8,
            "answer": 32,
            "hint": "4 × 8"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.py", host="0.0.0.0", port=8000, reload=True)
