import asyncio
import aio_eth
import time

URL = "https://rinkeby.infura.io/v3/b6fe23ef7add48d18d33c9bf41d5ad0c"


async def query_blocks():
    async with aio_eth.EthAioAPI(URL, max_tasks=100) as api:
        for i in range(10553978, 10553978 + 70):
            api.push_task({
                "method": "eth_getBlockByNumber",
                "params": [
                    hex(i), True
                ]
            })

        st = time.time()
        _ = await api.exec_tasks_async()
        et = time.time()
        print('time taken: ', et - st, ' seconds')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(query_blocks())
