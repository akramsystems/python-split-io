import asyncio
from splitio import get_factory_async
from splitio.exceptions import TimeoutException

from dotenv import load_dotenv
import os

load_dotenv()

split_api_key = os.getenv('SPLIT_API_KEY')
firm_id = '123'

async def main():
    factory = await get_factory_async(split_api_key)
    try:
        await factory.block_until_ready(5) # wait up to 5 seconds
    except TimeoutException:
        # Now the user can choose whether to abort the whole execution, or just keep going
        # without a ready client, which if configured properly, should become ready at some point.
        pass
    split = factory.client()

    treatment = await split.get_treatment(firm_id, 'ENABLE_MEETING_TYPE')
    
    if treatment == 'on':
        print('Meeting type is enabled')
    elif treatment == 'off':
        print('Meeting type is disabled')
    else:
        print("Error in split")



# Use asyncio.run to handle the event loop
asyncio.run(main())