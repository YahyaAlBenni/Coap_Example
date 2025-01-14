import asyncio
from aiocoap import *

async def main():
    server_uri = "coap://localhost:5684/server-data"
    context = await Context.create_client_context()

    while True:
        # Ask the user for input before requesting the server
        input("Press Enter to request the water level from the server...")

        # Send a GET request to the server to fetch the water level
        message = Message(code=Code.GET, uri=server_uri) #----client sends GET request to server----

        try:
            response = await context.request(message).response #----server responds with the stored water level
            print(f"Water Level from Server: {response.payload.decode('utf-8')}")
        except Exception as e:
            print(f"Error retrieving data: {e}")

if __name__ == "__main__":
    asyncio.run(main())