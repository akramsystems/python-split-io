from contextlib import asynccontextmanager
from fastapi import FastAPI
from split_client import SplitClientSingleton

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
