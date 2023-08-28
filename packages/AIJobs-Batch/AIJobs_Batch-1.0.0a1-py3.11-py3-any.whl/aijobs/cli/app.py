from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os

config = load_dotenv(".env")
app = FastAPI(title="AIJobs App")


@app.on_event("startup")
def startup():
    app.mongodb = MongoClient(os.environ["MONGODB_URI"])
    app.database = app.mongodb[os.environ["DB_NAME"]]
    print("Connected to MongoDB server")


@app.on_event("shutdown")
def shutdown():
    app.mongodb.close()
    print("Closed the connection to MongoDB server.")
