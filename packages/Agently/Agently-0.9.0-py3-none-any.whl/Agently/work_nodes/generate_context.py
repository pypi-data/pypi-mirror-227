def generate_context(runtime_ctx, **kwargs):
    session_runtime_ctx = kwargs["session_runtime_ctx"]
    context_messages = session_runtime_ctx.get("context_messages")
    use_context = runtime_ctx.get("use_context")
    if use_context:
        runtime_ctx.set("context_messages", context_messages)
    return

def export(agently):
    agently\
        .manage_work_node("generate_context")\
        .set_main_func(generate_context)\
        .set_runtime_ctx({
            "use_context": {
                "layer": "session",
                "alias": { "set": "use_context" },
            },
            "context_messages": {
                "layer": "session",
                "alias": {
                    "extend": "extend_context",
                    "get": "get_context",
                }
            },
        })\
        .register()
    return