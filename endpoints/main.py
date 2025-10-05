from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import fastapi.middleware.cors as CORSMiddleware
import os
# Suppress gRPC logs
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""


# Load environment variables
load_dotenv()



# Configure Gemini API
genai.configure(api_key=os.getenv("API_KEY")) # type: ignore

# Initialize FastAPI
app = FastAPI(title="Gemini Text Generator")

# Request model
class Prompt(BaseModel):
    text: str

app.add_middleware(
    CORSMiddleware.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_NAME = "gemini-2.5-flash"  # or "gemini-1.5-pro"

# for m in genai.list_models(): # type: ignore
#     print(m.name, "supports:", m.supported_generation_methods)

@app.post("/generate")
async def generate_text(prompt: Prompt):
    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME) # type: ignore
        response = model.generate_content(prompt.text)
        text_output = response.text if hasattr(response, "text") else "No response generated."
        return {"response": text_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
