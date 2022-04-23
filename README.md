## aio-eth
A simple python library that can be used to run large Web3 queries on [Ethereum blockchain](https://ethereum.org/en/) concurrently as per [Ethereum JSON-RPC specification](https://ethereum.org/en/developers/docs/apis/json-rpc/).

The library provides a bare minimal framework for expressing raw JSON-RPC queries as described in the Ethereum Specification and execute them together either concurrently (off-chain on the client side) or together as a batch (JSON-RPC batch specification on-chain). This method greatly reduces the time required to run large queries sequentially and thus can be used for use-cases where we need to index large number of transactions happening on ethereum blockchain in a local database for faster Web2 queries.

### Features
1. Provides interface for concurrent execution of large number of JSON-RPC queries
2. Provides interface for batched execution of large number of JSON-RPC queries
3. Provides complete flexibility to call any JSON-RPC method by allowing users to specify raw queries directly.

### Requirements:
1. Python 3.6+

### How to install:

1. From source:
```
git clone git@github.com:Narasimha1997/aio-eth.git
cd aio-eth
pip3 install -e .
```

2. From [PyPi](https://pypi.org/):
```
pip3 install aio-eth
``` 

### Examples:

1. Run tasks concurrently: This method will create a socket for each task on the client-side and executes the JSON-RPC calls concurrently. Under the hood, this method uses [aiohttp](https://docs.aiohttp.org/en/stable/) module. By this way you are using the client machine's resources and bandwidth to run queries by creating N concurrent sockets.

```python
import asyncio
import aio_eth
import time

URL = "https://rinkeby.infura.io/v3/b6fe23ef7add48d18d33c9bf41d5ad0c"

async def query_blocks():

    # create the API handle
    async with aio_eth.EthAioAPI(URL, max_tasks=100) as api:

        # express queries - example: get all transactions from 70 blocks
        # starting from 10553978
        for i in range(10553978, 10553978 + 70):

            # submit tasks to the task list, if `current tasks > max_tasks`
            # this method throws an exception.
            api.push_task({
                "method": "eth_getBlockByNumber",
                "params": [
                    hex(i), True
                ]
            })
        

        st = time.time()
        # execute the tasks together concurrently, outputs are returned in the same
        # order in which their corresponding queries where submitted.
        result = await api.exec_tasks_async()
        et = time.time()
        print('time taken: ', et - st, ' seconds')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(query_blocks())
```

Output:
```
time taken:  1.5487761497497559  seconds
```

2. Run tasks as batch: This method will submit the batch of queries to the connected Ethereum RPC server and expects the output of all the queries at once, unlike concurrent method, here you will be using only one socket as all the queries are submitted as batch. While Batch API is very useful, few providers do not support batch queries, so make sure your provider supports batch queries before using this.

```python
import asyncio
import aio_eth
import time

URL = "https://rinkeby.infura.io/v3/b6fe23ef7add48d18d33c9bf41d5ad0c"

async def query_blocks():

    # create the API handle
    async with aio_eth.EthAioAPI(URL, max_tasks=100) as api:

        # express queries - example: get all transactions from 70 blocks
        # starting from 10553978
        for i in range(10553978, 10553978 + 70):

            # submit tasks to the task list, if `current tasks > max_tasks`
            # this method throws an exception.
            api.push_task({
                "method": "eth_getBlockByNumber",
                "params": [
                    hex(i), True
                ]
            })
        

        st = time.time()
        # execute the tasks together as batch, outputs are returned in the same
        # order in which their corresponding queries where submitted.
        result = await api.exec_tasks_batch()
        et = time.time()
        print('time taken: ', et - st, ' seconds')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(query_blocks())
```
Output:
```
time taken:  3.698002576828003  seconds
```
It can be noted that using concurrent connects gives result in less time when compared to batch API, but Batch API can be helpful for large queries involving hundreds of tasks as opening many concurrent sockets while eat up the system's resources.

### Handling errors:
1. When using `exec_tasks_async` - each task can succeed or fail independently as they are executed concurrently, each item in the result contains a key called `success`, which is either `True` or `False`, if `success` is `False`, then a field called `exception` can be read to get the `Exception` object of the corresponding error.
2. When using `exec_tasks_batch`, all of the tasks can either succeed or fail as it is executed on the server side. For this reason, the method throws an exception on failure and must be handled externally.

### Maximum tasks size:
We can limit the number of tasks that can be allowed to be submitted at once by calling `set_max_tasks` method. By default it is set to 100. When we try to more tasks above this limit using `push_task` an exception is thrown. Example:

```python
async with aio_eth.EthAioAPI(URL, max_tasks=100) as api:
    ......
    # set max task size
    api.set_max_tasks(500)
    .......
```

### TODO:
1. Support Web Sockets channel

### Contributing
Please feel free to raise issues and submit PRs.