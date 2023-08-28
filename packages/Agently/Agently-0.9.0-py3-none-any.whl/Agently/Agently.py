from .RuntimeCtx import RuntimeCtx
from .WorkNodes import WorkNodes
from .Workflows import Workflows
from .Blueprint import Blueprint
from .Agent import Agent
from .work_nodes import generate_context, generate_prompt, assemble_request_messages, request

class Agently(object):
    def __init__(self):
        self.runtime_ctx = RuntimeCtx(None)
        self.work_nodes = WorkNodes(self.runtime_ctx)
        self.workflows = Workflows(self.runtime_ctx)
        return

    def manage_work_node(self, work_node_name):
        return self.work_nodes.manage_work_node(work_node_name)

    def set_workflow(self, workflow, *, name="default"):
        return self.workflows.set_workflow(name, workflow)

    def create_blueprint(self):
        return Blueprint(self)

    def create_agent(self, blueprint = None):
        return Agent(self, blueprint)

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

    def use(self, inject_funcs):
        if not isinstance(inject_funcs, list):
            if not callable(inject_funcs):
                raise Exception("[Agently use]: .use() must pass on a function list or a function.")
            else:
                inject_funcs = [inject_funcs]
        for inject_func in inject_funcs:
            if not callable(inject_func):
                raise Exception("[Agently use]: .use() must pass on a callable function.")
            else:
                inject_func(self)
        return self

def create_empty():
    return Agently()

def create():
    agently = Agently()
    agently.use([generate_context, generate_prompt, assemble_request_messages, request])
    agently.set_workflow(["generate_context", "generate_prompt", "assemble_request_messages", "request"])
    return agently