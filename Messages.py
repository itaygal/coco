from multiprocessing import Queue
import threading


class ReceiveMessage:
    __queue = None
    __waitCondition = None

    def __init__(self):
        super(ReceiveMessage, self).__init__()
        self.__queue = Queue()
        self.__wait_condition = threading.Condition()

    def send_message(self, msg):
        self.__queue.put(msg)
        with self.__wait_condition:
            self.__wait_condition.notifyAll()

    def get_message(self):
        if self.__queue.empty():
            with self.__wait_condition:
                self.__wait_condition.wait()
        return self.__queue.get()
