import threading
import traceback


class Thread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.args = args
        self.func = func
        self.error = None

    def run(self):
        try:
            self.func(*self.args)
        except Exception:
            self.error = traceback.format_exc()


class CommunicationThread(Thread):
    def __init__(self, func, args=None, variable_type=None):
        super().__init__(func, args)
        self.type = variable_type

        class InternalObject:
            def __init__(self):
                self.value = None

        self.safeObject = InternalObject()

    def run(self):
        try:
            self.safeObject.value = self.func(*self.args)
        except Exception:
            self.error = traceback.format_exc()

        if self.type is not None and not isinstance(self.safeObject.value, self.type):
            self.safeObject.value = None

    def retrieve_value(self):
        return self.safeObject.value

