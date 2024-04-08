from discord_py_api.Client import Client
from discord_py_api.Message import Message

if __name__ == "__main__":
    import maskpass

    # username = input("Enter username:\n> ")
    # password = maskpass.askpass("Enter password:\n> ", '*')
    # code = input("Enter auth code (leave blank if there is none):\n> ")

    # if code == "".strip(): code = None

    # user = User(username=username, password=password, auth_code=code)
    input_token = maskpass.askpass("Enter token:\n> ", '*')
    user = Client(token=input_token, debug=True)

    channel = input("Please enter a channel ID:\n> ")
    messages: list[Message] = user.get_messages(channel, limit=10)
    messages.reverse()

    for x in messages:
        print(f"[{x.author.display_name if x.author.display_name is not None else x.author.username}]: {x.content}")


# The following is purely experimental code.

# wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream

# async def loop(ws: websockets.WebSocketClientProtocol, messages: list):
#     while True:
#         x = await ws.recv()
#         messages.append(x)
#         os.system("clear")
#         for compressed in messages:
#             decompress_obj = zlib.decompressobj()
#             # try:
#             #     message = decompress_obj.decompress(compressed)
#             # except Exception as e:
#             #     message = e
#             message = compressed
#             print(message)
#
#
# async def main(token: str):
#     async with websockets.connect('wss://gateway.discord.gg/?encoding=json&v=9') as ws:
#         payload = json.dumps({'op': 2, 'd': {'token': token, 'capabilities': 16381, "compress": False}})
#         second_payload = json.dumps({"op": 37, "d": {"subscriptions": {"868121354698903592":
#                                                                            {"channels": {"1215297993515991081":
#                                                                                              [[0, 99]]
#                                                                                          }}}}})
#         x = await ws.send(payload)
#         await ws.send(second_payload)
#         messages = []
#
#         while True:
#             try:
#                 await loop(ws, messages)
#             except Exception as e:
#                 print(e)
#                 continue
#
#
# if __name__ == '__main__':
#     import maskpass
#
#     input_token = maskpass.askpass("Enter token:\n> ", '*')
#     asyncio.run(main(input_token))
