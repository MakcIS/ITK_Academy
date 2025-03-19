import json
import math
import multiprocessing
import os
from concurrent.futures import ThreadPoolExecutor
from random import randint
from time import perf_counter

import matplotlib.pyplot as plt


def generate_data(n):
    return [randint(1, 1000) for _ in range(n)]


list_numbers = generate_data(1000000)


def time_function(func, *args, **kwargs) -> tuple:
    strat = perf_counter()
    func(*args, **kwargs)
    end = perf_counter()
    return func.__name__, end - strat


def factorial_with_one_tread(numbers: list):
    for num in numbers:
        math.factorial(num)


def factorial_with_tread_pool(numbers: list):
    with ThreadPoolExecutor() as executor:
        executor.map(math.factorial, numbers)


def factorial_with_multip_pool(numbers: list):
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        pool.map(math.factorial, numbers)


def factorial_with_multip_process(numbers: list):
    def producer_func(queue: multiprocessing.Queue):
        for i in numbers:
            queue.put(i)
        queue.put(None)

    def consumer_func(queue: multiprocessing.Queue):
        while True:
            num = queue.get()
            if num is None:
                break
            math.factorial(num)

    queue = multiprocessing.Queue()

    producer = multiprocessing.Process(target=producer_func, args=(queue,))
    consumer = multiprocessing.Process(target=consumer_func, args=(queue,))

    producer.start()
    consumer.start()

    producer.join()
    producer.join()


x = []
y = []
result = {}
for func in [
    factorial_with_one_tread,
    factorial_with_tread_pool,
    factorial_with_multip_pool,
    factorial_with_multip_process,
]:
    name, value = time_function(func, list_numbers)
    result[name] = value
    x.append(name.split("with_")[1])
    y.append(value)

with open(os.path.dirname(__file__) + "/result.json", "w") as file:
    json.dump(result, file)

plt.bar(x, y, label="График выполнения функций")
plt.xlabel("Название функции", fontsize=10)
plt.ylabel("Время выполнения", fontsize=10)
plt.savefig(os.path.dirname(__file__) + "/grafik.png")
