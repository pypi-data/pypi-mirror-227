import queue
import copy

from .utils import inject_alias, set_default_runtime_ctx, EventEmitter
from .RuntimeCtx import RuntimeCtx

class Session(object):
    def __init__(self, agent):
        self.agent = agent
        self.runtime_ctx = RuntimeCtx(agent.runtime_ctx)
        self.work_nodes = self.runtime_ctx.get_all_above(domain="work_nodes")
        self.workflows = self.runtime_ctx.get_all_above(domain="workflows")
        listener = EventEmitter()
        self.listeners = [listener]
        self.listener_index = self.listeners.index(listener)
        self.final_result = {}
        inject_alias(self, "agent")
        inject_alias(self, "session")
        inject_alias(self, "request")
        set_default_runtime_ctx(self, "session")
        set_default_runtime_ctx(self, "request")
        self.is_working = False
        self.work_queue = queue.Queue()
        return

    def set(self, key, value, **kwargs):
        self.runtime_ctx.set(key, value, **kwargs)
        return self

    def get(self, key, **kwargs):
        self.runtime_ctx.get(key, **kwargs)
        return self

    def append(self, key, value, **kwargs):
        self.runtime_ctx.get(key, value, **kwargs)  
        return self

    def extend(self, key, value, **kwargs):
        self.runtime_ctx.extend(key, value, **kwargs)
        return self

    def on(self, event, handler, *, segment="default"):
        self.listeners[self.listener_index].on(event, handler, segment=segment)
        return self

    def addEventHandler(self, event, handler, *, segment="default"):
        self.listeners[self.listener_index].on(event, handler, segment=segment)
        return self

    def __start_next(self, data):
        data["listener"].stop()
        self.is_working = False
        listener, workflow_name, request_runtime_ctx = self.work_queue.get()
        self.is_working = True
        self.__start(listener, workflow_name, request_runtime_ctx)

    def __start(self, listener, workflow_name, request_runtime_ctx):
        if workflow_name in self.workflows:
            if not isinstance(self.workflows[workflow_name], list) or len(self.workflows[workflow_name]) == 0:
                raise Exception(f"[session start]: No work node in workflow { workflow_name }")
            listener.on("workflow_finish", self.__start_next)
            for work_node_name in self.workflows[workflow_name]:
                self.work_nodes[work_node_name]["main"](\
                    request_runtime_ctx,\
                    listener=listener,\
                    process = self.work_nodes[work_node_name]["process"],\
                    session_runtime_ctx = self.runtime_ctx,\
                    agent_runtime_ctx = self.agent.runtime_ctx\
                )
            listener.emit("workflow_finish", { "listener": listener })
        else:
            raise Exception(f'[session start]: No workflow named { workflow_name }')
        return

    def start(self, **kwargs):
        listener = self.listeners[self.listener_index]
        workflow_name = kwargs.get("workflow", "default")
        request_runtime_ctx = RuntimeCtx(self.runtime_ctx)
        if self.is_working:
            self.work_queue.put(( listener, workflow_name, request_runtime_ctx ))
        else:
            self.is_working = True
            self.__start( listener, workflow_name, request_runtime_ctx )
        listener = EventEmitter()
        self.listeners.append(listener)
        self.listener_index = self.listeners.index(listener)
        return

class Agent(object):
    def __init__(self, agently, blueprint = None):
        presettings = {}
        if blueprint:
            presettings = blueprint.runtime_ctx.get_all_domain().copy()
        self.runtime_ctx = RuntimeCtx(agently.runtime_ctx, presettings)
        inject_alias(self, "agent")
        set_default_runtime_ctx(self, "agent")
        return
    '''
    Basic RuntimeCtx Management
    '''
    def set(self, key, value, **kwargs):
        self.runtime_ctx.set(key, value, **kwargs)
        return self

    def get(self, key, **kwargs):
        self.runtime_ctx.get(key, **kwargs)
        return self

    def append(self, key, value, **kwargs):
        self.runtime_ctx.append(key, value, **kwargs)
        return self

    def extend(self, key, value, **kwargs):
        self.runtime_ctx.extend(key, value, **kwargs)
        return self
    '''
    Create Session
    '''
    def create_session(self):
        return Session(self)