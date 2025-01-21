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


# Вариант fetch_urls для работы с большим количеством входных данных

import aiohttp
import aiofiles
import asyncio
from asyncio import Queue



urls = [
    "https://example.com" for _ in range(10000)
]



async def get_status_for_url_or_zero(url: str, session) -> dict:
    data = {}
    try:
        async with session.get(url) as response:
            data.update({"url": url, "status_code": response.status})

    except (aiohttp.ClientError, asyncio.TimeoutError):
        data.update({"url": url, "status_code": 0})

    return data



async def consumer_worker(queue, session, f):
    print("Start consumer worker")

    while True:
        url = await queue.get()     # Получение url из очереди

        if url is None:     # Условие для прерывания цикла воркера
            break
        result = await get_status_for_url_or_zero(url, session)
        await f.write(f"{result}\n")
        queue.task_done()



async def fetch_urls(urls: list[str], file_path: str):
    queue = Queue()

    for url in urls:
        await queue.put(url)    # заполнение очереди

    async with aiohttp.ClientSession() as session, aiofiles.open(file_path, "w") as f:
        tasks = [asyncio.create_task(consumer_worker(queue, session, f)) for _ in range(5)]     # создание воркеров
        await queue.join()  # отмечаем задачу, как выполненную

    for _ in range(5):
        await queue.put(None)   # добавляем значения None в конец очереди, чтобы потом прервать воркеры
    await asyncio.gather(*tasks)    # добавляем в цикл воркеров




if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.json'))

