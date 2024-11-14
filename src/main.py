from fastapi import FastAPI

from src.controller.data_controller import router as data_router

app = FastAPI()

# Include the router for the categories endpoint under /api
app.include_router(data_router, prefix='/api')


@app.get('/')
def root():
    return {'message': 'Welcome to the Data Collection API'}
