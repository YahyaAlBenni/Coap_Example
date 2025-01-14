import asyncio
from aiocoap import *
from aiocoap import resource


class ServerDataHandler(resource.Resource):
    def _init_(self):
        super().__init__()
        self.water_level = None

    async def render_post(self, request):
        # Receive data from the controller
        self.water_level = request.payload.decode('utf-8') # ---- server receives the  POST request from the controller ----
        print(f"Updated Water Level: {self.water_level}")
        return Message(code=Code.CHANGED, payload=b"Data stored on server")

    async def render_get(self, request):
        # Serve the water level to the client
        if self.water_level:
            return Message(code=Code.CONTENT, payload=self.water_level.encode('utf-8'))
        else:
            return Message(code=Code.CONTENT, payload=b"No data available")

async def main():
    # Server runs as a CoAP server
    root = resource.Site()
    root.add_resource(['server-data'], ServerDataHandler())
    await Context.create_server_context(root, bind=("localhost", 5684))
    print("Server running on localhost:5684...")
    await asyncio.get_running_loop().create_future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
