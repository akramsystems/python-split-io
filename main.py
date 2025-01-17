from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Body
from split_client import SplitClientSingleton
from pydantic import BaseModel
from typing import Union

split_client = SplitClientSingleton()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize resources (startup)
    print("Starting up: Initializing Split client...")
    await split_client.initialize()
    print("Split client initialized.")
    yield
    # Cleanup resources (shutdown)
    print("Shutting down: Cleaning up Split client...")
    await split_client.shutdown()
    print("Split client shut down.")

# Pass the lifespan context manager to FastAPI
app = FastAPI(lifespan=lifespan)

@app.get("/get-treatment/{firm_id}/{feature_name}")
async def get_treatment(firm_id: str, feature_name: str):
    treatment = await split_client.get_treatment(firm_id, feature_name)
    return {"treatment": treatment}

# Define multiple schemas
class SchemaOnRequest(BaseModel):
    field1: str
    field2: int

class SchemaOffRequest(BaseModel):
    field1: str
    field3: float

# Dependency to select schema based on feature_name
async def get_schema(firm_id: str, feature_name: str, data: dict = Body(...)):
    treatment = await split_client.get_treatment(firm_id, feature_name)
    print(treatment)
    if treatment == "on":
        return SchemaOnRequest(**data)
    elif treatment == "off":
        return SchemaOffRequest(**data)
    else:
        raise HTTPException(status_code=400, detail="Invalid feature name")

# POST endpoint with dynamic schema
@app.post("/schema/{firm_id}/{feature_name}")
async def submit_data(firm_id: str, feature_name: str, data: Union[SchemaOnRequest, SchemaOffRequest] = Depends(get_schema)):
    # Process the data
    return {"message": "Data processed successfully", "data": data.model_dump()}