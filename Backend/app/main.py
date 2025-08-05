from fastapi import FastAPI
from app.withings.auth import router as withings_router
from app.fitbit.auth import router as fitbit_router
from app.fitbit.profile import router as fitbit_data_router
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
app.include_router(withings_router)
app.include_router(fitbit_router)
app.include_router(fitbit_data_router)

app.add_middleware(SessionMiddleware, secret_key="1234")
