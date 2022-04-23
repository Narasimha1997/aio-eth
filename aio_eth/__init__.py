import asyncio
import aiohttp


class EthAioAPI:

    def __init__(self, url: str, max_tasks=100):
        self.url = url
        self.current_tasks = []
        self.current_id = 0
        self.max_tasks = max_tasks

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err):
        await self.session.close()
        self.session = None

    async def tasklet(
        id: int,
        url: str,
        session: aiohttp.ClientSession,
        payload: dict
    ) -> dict:

        try:
            response = await session.post(
                url, json=payload,
                headers={"Content-Type": "application/json"}
            )

            json_resp = await response.json()
            json_resp['success'] = True

            return json_resp

        except Exception as e:
            return {"success": False, "exception": e, "id": id}

    def push_task(self, task: dict):

        if self.current_id >= self.max_tasks:
            raise Exception("maximum tasks exceeded")

        payload = {
            "jsonrpc": "2.0",
            "method": task["method"],
            "params": task["params"],
            "id": self.current_id
        }

        self.current_tasks.append(payload)
        self.current_id += 1

    async def exec_tasks_batch(self):
        try:
            response = await self.session.post(
                self.url, json=self.current_tasks, headers={
                    "Content-Type": "application/json"}
            )

            json_resp = await response.json()
            self.current_tasks.clear()
            self.current_id = 0

            return json_resp

        except Exception as e:
            raise e

    async def exec_tasks_async(self):
        fns = []
        for id, task_payload in enumerate(self.current_tasks):
            task_fn = EthAioAPI.tasklet(
                id, self.url, self.session, task_payload)
            fns.append(task_fn)

        outputs = await asyncio.gather(*fns, return_exceptions=True)

        self.current_tasks.clear()
        self.current_id = 0
        return outputs

    def set_max_tasks(self, n: int):
        self.max_tasks = n
