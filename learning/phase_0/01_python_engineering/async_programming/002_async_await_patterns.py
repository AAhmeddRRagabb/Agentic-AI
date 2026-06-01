# ------------------------------------------------------
# Alhamdulillah
# Exercising Common Async / Await Patterns
# ------------------------------------------------------

def print_title(title):
    title = f" {title} ".center(100, "=")
    print(title)

def print_sep():
    print()
    print()



async def fetch_data(id: int):
    await asyncio.sleep(1)
    return {"data": id * 10}

import time
def get_time_now():
    return time.time()



def run(main):
    start_time = get_time_now()
    asyncio.run(main = main())
    taken_time = get_time_now() - start_time
    print(f">> Taken time: {taken_time} s")
    print_sep()




# 1.0 Basic Async Function Pattern
import asyncio

print_title("1.0 Basic Async Func Pattern")

async def main():
    result = await fetch_data(5)
    print(result)

run(main)


# 2.0 Run many tasks concurrently & wait for all of them
import asyncio


print_title("2.0 Many Concurrent Tasks")

async def main():
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3),
    )

    print(results)

run(main)



# 3.0 Task Group
print_title("3.0 Task Group")
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data(1))
        task2 = tg.create_task(fetch_data(2))

    print(task1.result())
    print(task2.result())

run(main)


# 4.0 Lock
print_title("4.0 Lock Pattern")
lock = asyncio.Lock()
shared_resource = 0

async def update_resource(id):
    global shared_resource

    async with lock:
        print(f">> Process: {id} Entered")
        shared_resource = id
        
        print(f">> Process: {id} delayed but still hold the lock")
        await asyncio.sleep(1)

        print(f">> Process: {id} leaves the critical section")

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(update_resource(3))
        task2 = tg.create_task(update_resource(5))

    print(task1.result())
    print(task2.result())

run(main)


# 5.0 Producer - Consumer
print_title("5.0 Producer-Consumer Pattern")

queue = asyncio.Queue()

async def produce(id):
    await queue.put(id)

async def consume():
    item = await queue.get()
    queue.task_done()

    return item

async def main():
    async with asyncio.TaskGroup() as tg:
        producers = [tg.create_task(produce(i)) for i in range(5)]
    

    for p in producers:
        print(p.result())

    await asyncio.sleep(1)

    async with asyncio.TaskGroup() as tg:
        consumers = [tg.create_task(consume()) for _ in range(5)]
    
    for c in consumers:
        print(c.result())

run(main)


# 6.0 Time Out: do now wait forever
print_title("6.0 Timeout")

async def fetch_data(id):
    await asyncio.sleep(3)
    return {"data": id}

async def main():
    try:
        result = await asyncio.wait_for(fetch_data(5), timeout = 2)

    except asyncio.TimeoutError:
        print(">> Operation is very slow")

run(main)

# 7.0 Semaphore: run many tasks, but limit how many run at the same time
print_title("7.0 Semaphore")
semaphore = asyncio.Semaphore(5)


async def fetch_with_limit():
    async with semaphore:
        return await fetch_data(3)

run(fetch_with_limit)