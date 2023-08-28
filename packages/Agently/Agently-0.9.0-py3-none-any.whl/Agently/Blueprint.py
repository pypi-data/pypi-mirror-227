from .RuntimeCtx import RuntimeCtx
from .WorkNodes import WorkNodes
from .Workflows import Workflows
from .utils import inject_alias, set_default_runtime_ctx

class Blueprint(object):
    def __init__(self, agently):
        self.runtime_ctx = RuntimeCtx(agently.runtime_ctx, kwargs)
        self.work_nodes = WorkNodes(self.runtime_ctx)
        self.workflows = Workflows(self.runtime_ctx)

    def manage_work_node(self, work_node_name):
        return self.work_nodes.manage_work_node(work_node_name)

    def set_workflow(self, workflow, **kwargs):
        workflow_name = kwargs.get("name", "default")
        return self.workflows.set_workflow(workflow_name, workflow)

    def set(self, key, value, **kwargs):
        self.runtime_ctx.set(key, value, **kwargs)
        return self

    def append(self, key, value, **kwargs):
        self.runtime_ctx.append(key, value, **kwargs)
        return self

    def init(self):
        inject_runtime_ctx_settings(self, "agent")
        set_default_runtime_ctx(self, "agent")
        return