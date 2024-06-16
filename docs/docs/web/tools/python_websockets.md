# Python websockets

## Example

```py
async def main(uri):
    async with websockets.connect(uri) as ws:
        # <payload> 的 type 是 str
        await ws.send(<payload>)

        result = await ws.recv()
        # result 的 type 是 str

        # 可以先把 ws.send 把要 send 的 payload 全部 send 完，然後再慢慢 ws.recv()，這樣速度比較快
        # 不過 ws.recv() 需要一條一條照順序的接收


# 如果 JS 裡面寫
# 
# ```js
# const socket = new WebSocket("ws://<server>:{port}");
# ```
# 
# 那就代表 uri 會是 ws://<server>:{port}/ws 或 wss://<server>:{port}/ws
# 如果原本網站是用 HTTP 那就是 ws，如果是 HTTPS 的話就用 wss
uri = 'wss://<server>:{port}/ws'
asyncio.get_event_loop().run_until_complete(main(uri))
```
