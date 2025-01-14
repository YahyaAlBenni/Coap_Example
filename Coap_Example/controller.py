import asyncio
import random
from aiocoap import resource, Context, Message, Code


class SensorDataHandler(resource.Resource):
    def __init__(self):
        super().__init__()
        self.latest_data = None

    async def handle_sensor_data(self):
        """Simulate receiving random data from the water level sensor every 30 seconds."""
        while True:
            # Generate random data between 10 and 100
            self.latest_data = random.randint(10, 100)
            print(f"Received Data from Sensor: {self.latest_data}")

            # Simulate forwarding data to the server
            await self.forward_data_to_server(self.latest_data)

            # Wait for 30 seconds
            await asyncio.sleep(30)

    async def forward_data_to_server(self, data):
        """Forward the received data to the server."""
        server_uri = "coap://localhost:5684/server-data"
        context = await Context.create_client_context()
        message = Message(code=Code.POST, uri=server_uri, payload=str(data).encode('utf-8'))

        try:
            response = await context.request(message).response
            print(f"Server Response: {response.code}")
        except Exception as e:
            print(f"Error forwarding data to server: {e}")

    async def render_get(self, request):
        """Serve the latest data to any client requesting it."""
        if self.latest_data is not None:
            return Message(code=Code.CONTENT, payload=str(self.latest_data).encode('utf-8'))
        else:
            return Message(code=Code.CONTENT, payload=b"No data available")


async def main():
    # Create a CoAP server
    root = resource.Site()
    handler = SensorDataHandler()
    root.add_resource(['sensor-data'], handler)
    await Context.create_server_context(root, bind=("localhost", 5683))
    print("Controller running...")

    # Start simulating sensor data
    await handler.handle_sensor_data()


if __name__ == "__main__":
    asyncio.run(main())
