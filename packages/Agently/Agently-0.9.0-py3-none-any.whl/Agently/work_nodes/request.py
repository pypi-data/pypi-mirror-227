from .request_process import update_process

def request(runtime_ctx, **kwargs):
    process = kwargs["process"]
    listener = kwargs["listener"]
    llm_name = runtime_ctx.get("llm_name")

    request_data = process["prepare_request_data"][llm_name](runtime_ctx)

    if runtime_ctx.get("is_debug"):
        print("[REQUEST]")
        print(request_data["data"]["messages"])

    is_streaming = runtime_ctx.get("is_streaming")
        
    if not is_streaming:
        response = process["request_llm"][llm_name](request_data).text
        if runtime_ctx.get("is_debug"):
            print("[RESPONSE]")
            print(response)
    else:
        response = process["streaming_llm"][llm_name](request_data)
    process["emit_result"][llm_name](is_streaming, response, listener)
    return

def export(agently):
    agently\
        .manage_work_node("request")\
        .set_main_func(request)\
        .set_runtime_ctx({
            "llm_name": {
                "layer": "agent",
                "alias": { "set": "set_llm_name" },
                "default": "GPT"
            },
            "llm_url": {
                "layer": "agent",
                "alias": { "set_kv": "set_llm_url" },
            },
            "llm_auth": {
                "layer": "agent",
                "alias": { "set_kv": "set_llm_auth" },
            },
            "proxy": {
                "layer": "agent",
                "alias": { "set": "set_proxy" },
            },
            "is_streaming": {
                "layer": "session",
                "alias": { "set": "set_streaming" },
                "default": False,
            },
            "request_options": {
                "layer": "session",
                "alias": { "set": "set_request_options" },
            },
        })\
        .register()
    update_process(agently.manage_work_node("request"))
    return