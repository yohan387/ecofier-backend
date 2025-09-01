from fastapi import FastAPI
from routes import utilisateur
from routes import clients
from routes import pesees
from dotenv import load_dotenv
from database import init_db, close_db
from contextlib import asynccontextmanager

app = FastAPI(
    title="Backend Ecofier",
)


app.include_router(clients.router)
app.include_router(utilisateur.router)
app.include_router(pesees.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)