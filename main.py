from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from spotify.spotify import getTrack


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    trackId = await getTrack()
    return templates.TemplateResponse("index.html", {"request": request, "trackId": trackId})

@app.get("/api/track")
async def test():
    return {"trackId": await getTrack()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)