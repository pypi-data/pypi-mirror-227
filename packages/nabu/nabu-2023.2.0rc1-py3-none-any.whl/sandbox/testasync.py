import asyncio
from threading import Thread
from time import sleep

def start_background_loop(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return "OK"


def main():
    loop = asyncio.new_event_loop()
    t = Thread(target=start_background_loop, args=(loop,), daemon=True)
    t.start()


    task = asyncio.run_coroutine_threadsafe(
        say_after(2, "hello"),
        loop
    )

    for i in range(10):
        sleep(0.5)
        print("Main thread doing stuff")

    print(task.result())
    loop.stop()

    # t.join()



if __name__ == "__main__":
    main()