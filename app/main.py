from fastapi import FastAPI

from routers import login
from routers import signup
from routers import agent
from routers import schedule
from routers import booking
from dependencies.database import Base, engine

description = """
Con esta API tienes una agenda online

## Leeme

- Crea un usuario desde el endpoint **/signup** con tu email y contraseña y un rol (admin, client)
- Inicia sesión desde el endpoint **/login**
- Crea uno o varios agentes desde el endpoint **/agent** a traves de un metodo POST
- Puedes ver los agentes creados desde el endpoint **/agent** a traves de un metodo GET
- Con el endpoint  **/schedule** puedes ver la disponiblidad para cada agente y crear una cita
- Con el endpoint **/booking** puedes ver las citas agendadas y actualizarlas o eliminarlas
"""

app = FastAPI(
    title="Mous",
    description=description,
    summary="Ayuda a organizar tus citas",
    version="0.0.1",
)

app.include_router(login.router)
app.include_router(signup.router)
app.include_router(agent.router)
app.include_router(schedule.router)
app.include_router(booking.router)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
