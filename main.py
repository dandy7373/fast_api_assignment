import imp
from fastapi import FastAPI
from utils.db_connection import connection
from router.authentication import authenticationRouter
from router.upload_module import upload_router

app= FastAPI()

app.include_router(authenticationRouter,tags=['Authentication'])
app.include_router(upload_router,tags=['Upload'])