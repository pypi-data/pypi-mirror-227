import queue
import threading

class EventEmitter:
    def __init__(self):
        self.event_queue = queue.Queue()
        self.listeners = {}
        self.stop_flag = False
        self.event_worker_thread = threading.Thread(target=self._process_events)
        self.event_worker_thread.start()

    def _process_events(self):
        while not self.stop_flag:
            event, args, kwargs = self.event_queue.get()
            segment = kwargs.get("segment", "default")
            if event in self.listeners[segment]:
                for listener in self.listeners[segment][event]:
                    listener(*args)
        return

    def stop(self):
        self.stop_flag = True
        return

    def on(self, event, listener, *, segment="default"):
        if segment not in self.listeners:
            self.listeners.update({ segment: {} })
        if event not in self.listeners[segment]:
            self.listeners[segment].update({ event: [] })
        self.listeners[segment][event].append(listener)
        return

    def emit(self, event, *args, **kwargs):
        self.event_queue.put((event, args, kwargs))
        return