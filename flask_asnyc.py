import time
import asyncio
from flask import Flask
from threading import Thread

app = Flask(__name__)

task_nr = 0



def do_some_work(x, attempts=0):
    print("Task %s, Waiting %s" % (str(attempts), str(x)))
    time.sleep(x)
    print("Done Task %s" % attempts)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        # Canceling pending tasks and stopping the loop
        asyncio.gather(*asnycio.Task.all_tasks()).cancel()

        # Stopping the loop
        loop.close()

        # Received Ctrl+C
        loop.close()

worker_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(worker_loop,))
t.start()

@app.route('/')
def hello():
    return "Hello World"

@app.route('/<timer>')
def timed_app(timer):
    global task_nr
    task_nr += 1
    worker_loop.call_soon_threadsafe(do_some_work, int(timer), task_nr)
    return("Starting timer for %d seconds" % int(timer))

if __name__ == '__main__':
    app.run()
