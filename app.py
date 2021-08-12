import json
import asyncio
import websockets

from image import Image


async def accept(websocket, path):
    while True:
        data = await websocket.recv()
        try:
            json_data = json.loads(data)
            image = Image(websocket, json_data['image'])
            await image.main()
        except json.decoder.JSONDecodeError:
            pass


def main():
    start_server = websockets.serve(accept, '192.168.137.1', 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
