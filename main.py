from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import httpx

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your front-end origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def fetch_content(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text


@app.get("/scrape/bbc")
async def scrape_bbc(url: str):
    try:
        content = await fetch_content(url)
        soup = BeautifulSoup(content, "html.parser")

        # Collect all text from BBC paragraphs
        paragraphs = soup.find_all("p")  # Get all <p> tags
        text_array = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]

        return {"paragraphs": text_array}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scrape/cnn")
async def scrape_cnn(url: str):
    try:
        content = await fetch_content(url)
        soup = BeautifulSoup(content, "html.parser")

        # Collect all text from CNN paragraphs
        paragraphs = soup.find_all("p")  # Get all <p> tags
        text_array = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]

        return {"paragraphs": text_array}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
