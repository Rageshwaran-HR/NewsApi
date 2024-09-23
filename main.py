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
async def bbc(url: str):
    try:
        content = await fetch_content(url)
        soup = BeautifulSoup(content, "html.parser")

        # Example selector, adjust as needed
        headline = soup.find("h1")
        if headline is None:
            raise ValueError("Failed to find the headline in the article.")

        title = headline.text.strip()
        return {"title": title}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scrape/cnn")
async def cnn(url: str):
    try:
        content = await fetch_content(url)
        soup = BeautifulSoup(content, "html.parser")

        # Example selector, adjust as needed
        headline = soup.find("h1")
        if headline is None:
            raise ValueError("Failed to find the headline in the article.")

        title = headline.text.strip()
        return {"title": title}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
