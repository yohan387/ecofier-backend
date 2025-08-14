from fastapi import FastAPI
from routes import utilisateur
from routes import clients
from routes import pesees


app = FastAPI(
    title="Backend Ecofier"
)

app.include_router(clients.router)
app.include_router(utilisateur.router)
app.include_router(pesees.router)

