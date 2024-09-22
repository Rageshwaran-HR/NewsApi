from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/scrape/cnn")
async def cnn(url: str = Query(None, description="The URL to scrape")):
    print(f"Scraping {url}")
    try:
        res = requests.get(url)
        res.raise_for_status()
        cnt = ""

        soup = BeautifulSoup(res.content, "html.parser")
        ath = soup.find("div", {"class": "headline__sub-text"}).find("div", {"class": "byline__names"}).text.strip()
        vid = json.loads(soup.find("div", {"class": "video-resource"})['data-fave-thumbnails'])
        uri = vid['big']['uri'].split('?')[0]
        ttl = soup.find("h1", {'class': 'headline__text'}).text.strip(" \n")
        art = soup.find("div", {'class': 'article__content'})
        for par in art.findAll("p", {"class": "paragraph"}):
            cnt += f"{par.text.strip()}\n"
        return {"title": ttl, "cover": uri, "content": cnt, "author": ath}
    except requests.exceptions.RequestException as e:
        return {"message": f"Error: {e}"}


@app.get("/scrape/bbc")
async def bbc(url: str = Query(None, description="The URL to scrape")):
    print(f"Scraping {url}")
    try:
        res = requests.get(url)
        res.raise_for_status()
        cnt, ath = "", ""

        soup = BeautifulSoup(res.content, "html.parser")
        atb = soup.find("div", {"data-component": "byline-block"}).findAll("span")
        for dta in range(len(atb[::2])):
            ath += f"{atb[dta].text.strip()}: {atb[dta + 1].text.strip()}\n"
        # vid = json.loads(soup.find("div", {"class": "video-resource"})['data-fave-thumbnails'])
        # uri = vid['big']['uri'].split('?')[0]
        ttl = soup.find("div", {'data-component': 'headline-block'}).find("h1").text.strip(" \n")
        art = soup.findAll("div", {'data-component': 'text-block'})
        for bod in art:
            for par in bod.findAll("p"):
                cnt += f"{par.text.strip()}\n"
        return {"title": ttl, "content": cnt, "author": ath}
    except requests.exceptions.RequestException as e:
        return {"message": f"Error: {e}"}

