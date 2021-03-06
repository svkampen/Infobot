"""
Threads module
"""

from threading import Thread
import datetime
from queue import Queue
import traceback
import sys

def get_core(item):
    if not hasattr(item, "__core__"):
        return False
    return item.__core__

class HandlerThread(Thread):
    def __init__(self, bot, lock):
        self.bot = bot
        self.queue = Queue()
        self.lock = lock
        super().__init__()

    def run(self):
        while True:
            try:
                items = None
                args = self.queue.get()
                with self.lock:
                    items = self.bot.__irccallbacks__[args[0]]
                
                for item in items:
                    if not get_core(item):
                        if self.bot.verbose:
                            print("[command thread:%s] calling fn %s" % (datetime.datetime.utcnow(), item.__name__))
                        item(self.bot, *(args[1]))

            except BaseException as e:
                if not isinstance(e, SystemExit) and not isinstance(e, KeyboardInterrupt):
                    traceback.print_exc()

    def push(self, cname, *args):
        self.queue.put(tuple([cname] + list(args)))
