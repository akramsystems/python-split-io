import asyncio
from splitio import get_factory_async
from splitio.exceptions import TimeoutException
import os
from dotenv import load_dotenv

load_dotenv()

class SplitClientSingleton:
    def __init__(self):
        self._initialized = False
        self.factory = None
        self.client = None

    async def initialize(self):
        if not self._initialized:
            split_api_key = os.getenv("SPLIT_API_KEY")
            self.factory = await get_factory_async(split_api_key)
            try:
                await self.factory.block_until_ready(5)  # Wait up to 5 seconds
            except TimeoutException:
                print("Split client initialization timed out.")
            self.client = self.factory.client()
            self._initialized = True

    async def get_treatment(self, firm_id, feature_name):
        if not self._initialized:
            raise RuntimeError("Split client is not initialized.")
        return await self.client.get_treatment(firm_id, feature_name)

    async def shutdown(self):
        if self.client:
            await self.client.destroy()
