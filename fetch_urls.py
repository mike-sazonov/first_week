# Напишите асинхронную функцию fetch_urls, которая принимает список URL-адресов и возвращает словарь,
# где ключами являются URL, а значениями — статус-коды ответов.
# Используйте библиотеку aiohttp для выполнения HTTP-запросов.
#
# Требования:
#
# - Ограничьте количество одновременных запросов до 5.
# - Обработайте возможные исключения (например, таймауты, недоступные ресурсы) и присвойте соответствующие статус-коды
#   (например, 0 для ошибок соединения).
# - Сохраните все результаты в файл

import aiohttp
import aiofiles
import asyncio



urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
]




async def get_status_for_url_or_zero(url: str, session) -> dict:
    data = {}
    try:
        async with session.get(url) as response:
            data.update({"url": url, "status_code": response.status})
    except (aiohttp.ClientError, asyncio.TimeoutError):
        data.update({"url": url, "status_code": 0})

    return data


async def fetch_urls(urls: list[str], file_path: str):
    semaphore = asyncio.Semaphore(5)

    async with aiohttp.ClientSession() as session:
        async with semaphore:
            result = await asyncio.gather(
                *(asyncio.create_task(get_status_for_url_or_zero(url, session)) for url in urls)
            )

    async with aiofiles.open(file_path, "w") as f:
        await asyncio.gather(*(asyncio.create_task(f.write(f"{res_dict}\n")) for res_dict in result))


if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.json'))

