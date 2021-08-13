import json
import asyncio
import websockets

from image import Image


async def accept(websocket, path):
    while True:
        data = await websocket.recv()
        try:
            json_data = json.loads(data)
            if json_data['process'] == 0:  # healthcheck
                await websocket.send('{"progress": 0, "message": "연결 성공"}')
            elif json_data['process'] == 1:  # process cv & ocr
                image = Image(websocket, json_data['image'])
                await image.main()
            else:
                pass
        except json.decoder.JSONDecodeError:
            pass


def main():
    start_server = websockets.serve(accept, None, 5000, max_size=10000000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
