# ------------------------------------------------------
# Alhamdulillah
# Async Programming in Python
# ------------------------------------------------------


# -------------------------------------- ASync Programming --------------------------------------
# -- Basic Idea

# ---> Instead of blocking the program while waiting for I/O operations,
#      async programming allows Python to (pause the current task [coroutine] in Python) and run another task.
#      the current task is paused in Python, but is running outside

# ---> Async VS Threads VS Processes [Python]
#      - Async:
#        Best for I/O-bound tasks with a lot of waiting,
#        such as API calls, network requests, database queries, and file operations.
#        Usually runs in one thread using an event loop.
#
#      - Threads:
#        Useful for I/O-bound tasks too, especially when using blocking libraries.
#        Threads share the same memory space, so sharing data is easy,
#        but you must be careful with race conditions.
#        In CPython, threads are usually not ideal for CPU-heavy parallelism because of the GIL.
#
#      - Processes:
#        Best for CPU-bound tasks.
#        Each process has separate memory and can run truly in parallel on multiple CPU cores.
#        Useful for heavy computation, image processing, ML preprocessing, etc.

# ---> Event Loop:
#      - The event loop manages multiple async tasks.
#      - Each task runs until it reaches an await point.
#      - If the task needs to wait for I/O, it gives control back to the event loop.
#      - The event loop then runs another ready task.
#      - When the waiting operation is ready, the task resumes from where it stopped.

# ---> Resources
#      - https://www.youtube.com/watch?v=Qb9s3UiMSTA&t=143s
# ---------------------------------------------------------------------------------------------------


import asyncio, time

def print_title(title):
    title = f" {title} ".center(100, "=")
    print(title)

def print_sep():
    print()
    print()


# print_title("1.0 Basic Async Function")
# async def main():
#     print("from ASync main which returns a Co-routine object")


# asyncio.run(main())
# print_sep()


# print_title("2.0 Awaiting & Executing Co-routines")
# async def fetch_data(delay):
#     """Simulating waiting for data"""
#     print(">> Fetching data...")
#     await asyncio.sleep(delay)

#     print(">> Fetched data...")
#     return {
#         "data" : [1, 2, 3]
#     }

# async def main():
#     print(">>> Starting of main co-routine:")

#     # creating a Co-routine for the task
#     task = fetch_data(2)

#     # execute the co-routine
#     result = await task

#     print(f"\tData Received: {result}")

#     print(">>> Ending of main co-routine")
#     print(50 * '=')


# asyncio.run(main())
# print_sep()



# print_title("3.0 Another Example to illustrate the difference between [Creating Co-routines] & [Executing them]")
# async def fetch_data(delay, id):
#     print("- Fetching data with id:", id)
#     await asyncio.sleep(delay)
#     print("- Data Fetched Correctly")
#     return {
#         "data": [id, id + 5, id + 10]
#     }


# async def main():
#     print(">>> Starting of main co-routine:")

#     # creating tasks [co-routines] -> will not be executed till awaiting them
#     task1 = fetch_data(2, 5)
#     task2 = fetch_data(2, 10)

#     # executing
#     data1 = await task1
#     print(f"\tData Received: {data1}")

#     data2 = await task2
#     print(f"\tData Received: {data2}")

#     print(">>> Ending of main co-routine")

# asyncio.run(main())
# print_sep()


# print_title("4.0 Creating tasks that can work con-currently")
# async def main():
#     print(">>> Starting of main co-routine:")

#     task1 = asyncio.create_task(fetch_data(2, 1))
#     task2 = asyncio.create_task(fetch_data(2, 15))
#     task3 = asyncio.create_task(fetch_data(2, 100))

#     data1 = await task1
#     data2 = await task2
#     data3 = await task3

#     print(data1, data2, data3)

#     print(">>> Ending of main co-routine")

# start_time = time.time()
# asyncio.run(main())
# time_taken = (time.time() - start_time)
# print(f">>> Time taken: {time_taken} s")  # note that, task 1 was busy -> it goes to task 2 and so on
# print_sep()


# async def main():
#     print(">>> Starting of main co-routine:")

#     task1 = asyncio.create_task(fetch_data(2, 1))
#     task2 = asyncio.create_task(fetch_data(2, 15))

#     # here, will wait for task1 & task2 because task3 is not created yet
#     data1 = await task1
#     data2 = await task2


#     task3 = asyncio.create_task(fetch_data(2, 100))
#     data3 = await task3

#     print(data1, data2, data3)

#     print(">>> Ending of main co-routine")

# start_time = time.time()
# asyncio.run(main())
# time_taken = (time.time() - start_time)
# print(f">>> Time taken: {time_taken} s") 
# print_sep()


# print_title("5.0 Gathering Tasks")
# async def fetch_data(delay, id):
#     print("- Fetching data with id:", id)
#     await asyncio.sleep(delay)
#     print("- Data Fetched Correctly")
#     return {
#         "data": [id, id + 5, id + 10]
#     }

# async def main():
#     print(">>> Starting of main co-routine:")

#     # running all tasks concurrently together
#     # gather function does not auto handle errors
#     # if one task fail --> the others may complete
#     results = await asyncio.gather(fetch_data(2, 1), fetch_data(2, 20), fetch_data(2, 100))

#     for result in results:
#         print(result, end = "\t")
#     print()
#     print(">>> Ending of main co-routine")

# start_time = time.time()
# asyncio.run(main())
# time_taken = (time.time() - start_time)
# print(f">>> Time taken: {time_taken} s") 
# print_sep()



# async def main():
#     print(">>> Starting of main co-routine:")

#     tasks = []

#     # task group handel errors
#     # if one task fail -> all fail
#     # grouped tasks block other code, but concurrent with each other. So code after these tasks [say three tasks]
#     # will not be executed until the three have been exectued
#     async with asyncio.TaskGroup() as tg:
#         for idx, sleep_time in enumerate([2, 2, 2], start = 1):
#             task = tg.create_task(fetch_data(sleep_time, idx))
#             tasks.append(task)
        
#     results = [task.result for task in tasks]

#     for result in results:
#         print(result, end = "\t")
#     print()
#     print(">>> Ending of main co-routine")

# start_time = time.time()
# asyncio.run(main())
# time_taken = (time.time() - start_time)
# print(f">>> Time taken: {time_taken} s") 
# print_sep()



print_title("6.0 Tasks Synchorization")
# useful for executing critical sections

shared_resource = 0

lock = asyncio.Lock()

async def modify_shared_resource(name, val):
    global shared_resource

    async with lock:
        print(f"Resource Before Modification: {shared_resource}")

        print(f">> Modifying using: {name}")
        shared_resource = val

        await asyncio.sleep(1) # other routines still cannot enter
        print(f"Resource After Modification: {shared_resource}")
        print()
        

temp_tasks = {
    "five" : 5,
    "four" : 4,
    "three": 3
}
async def main():
    await asyncio.gather(*(modify_shared_resource(name, val) for name, val in temp_tasks.items()))

asyncio.run(main())


