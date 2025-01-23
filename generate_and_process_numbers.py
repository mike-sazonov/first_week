# Разработайте программу, которая выполняет следующие шаги:
#
# Сбор данных:
#
# Создайте функцию generate_data(n), которая генерирует список из n случайных целых чисел в диапазоне от 1 до 1000.
# Например, generate_data(1000000) должна вернуть список из 1 миллиона случайных чисел.
#
# Обработка данных:
# Напишите функцию process_number(number), которая выполняет вычисления над числом. Например, вычисляет факториал числа
# или проверяет, является ли число простым. Обратите внимание, что обработка должна быть ресурсоёмкой,
# чтобы продемонстрировать преимущества мультипроцессинга.
#
# Параллельная обработка:
# Используйте модули multiprocessing и concurrent.futures для параллельной обработки списка чисел.
#
# Реализуйте три варианта:
#
# - Вариант А: Ипользование пула потоков с concurrent.futures.
#
# - Вариант Б: Использование multiprocessing.Pool с пулом процессов, равным количеству CPU.
#
# - Вариант В: Создание отдельных процессов с использованием multiprocessing.Process и очередей (multiprocessing.Queue)
#   для передачи данных.


from random import randint
from datetime import datetime

from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import Pool, Process, Queue, cpu_count

def time_decor(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        print(datetime.now() - start)
        return res
    return wrapper


def generate_data(n) -> list[int]:
    return [randint(1, 1000) for _ in range(n)]


def process_number(number) -> bool:
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True


#  стандартное вычисление
@time_decor
def base() -> list[bool]:
    res = []
    for i in numbers:
        res.append(process_number(i))
    return res


#  С применением пула процессов
@time_decor
def process_pool() -> list[bool]:
    with Pool(processes=cpu_count()) as pool:
        res = list(pool.map(process_number, numbers))
        return res


#  С применением пула потоков
@time_decor
def thread_pool() -> list[bool]:
    with ThreadPoolExecutor() as executor:
        res = list(executor.map(process_number, numbers))
        return res



def worker(input, output):
    """Функция, выполняемая рабочими процессами"""
    for func, n in iter(input.get, 'STOP'):
        result = func(n)
        output.put(result)

# Создание отдельных процессов с использованием multiprocessing.Process и очередей (multiprocessing.Queue)
@time_decor
def process_queue() -> list[bool]:
    res = []
    NUMBER_OF_PROCESSES = cpu_count()
    TASKS = [(process_number, number) for number in numbers]

    # Создание очередей
    task_queue = Queue()
    done_queue = Queue()


    # Запуск рабочих процессов
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Заполнение очереди заданий
    for task in TASKS:
        task_queue.put(task)

    # Получение результатов
    for i in range(len(TASKS)):
        res.append(done_queue.get())


    # Говорим дочерним процессам остановиться
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    return res


numbers = generate_data(1000000)


# results = base()
# results = process_pool()
# results = thread_pool()
results = process_queue()


# Запись полученных данных в файл
with open("./data.txt", "w") as f:
    for r in results:
        f.write(f"{r}\n")