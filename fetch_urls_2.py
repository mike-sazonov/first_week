import aiohttp
import aiofiles
import asyncio
import json
import concurrent.futures

from json import JSONDecodeError

# Вариант fetch_urls для обработки данных большого объёма


urls = [
    "https://jsonplaceholder.typicode.com/todos" for _ in range(100)
]

def parse_json(data):
    res = json.loads(data)
    # здесь можно добавить логику работы с полученным json
    return res





async def get_status_for_url_or_zero(loop, url: str, session) -> dict:
    data = {}
    try:
        async with session.get(url) as response:
            try:
                # обработка функции парсинга в отдельном процессе из пула процессов
                with concurrent.futures.ProcessPoolExecutor() as pool:
                    _ = await loop.run_in_executor(pool, parse_json, await response.text())
            except JSONDecodeError:
                pass

            data.update({"url": url, "status_code": response.status})
    except (aiohttp.ClientError, asyncio.TimeoutError):
        data.update({"url": url, "status_code": 0})

    return data


async def fetch_urls(urls: list[str], file_path: str):
    loop = asyncio.get_running_loop()

    async with aiohttp.ClientSession() as session:
            result = await asyncio.gather(
                *(get_status_for_url_or_zero(loop, url, session) for url in urls)
            )

    async with aiofiles.open(file_path, "w") as f:
        await asyncio.gather(*(asyncio.create_task(f.write(f"{res_dict}\n")) for res_dict in result))


if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.json'))