# -- coding: utf8 --

import requests
import sseclient
import json

'''
OpenAI GPT
'''
def prepare_request_data_gpt(runtime_ctx):
    #default request_data
    request_data = {
        "llm_url": "https://api.openai.com/v1/chat/completions",
        "data": {
            "model": "gpt-3.5-turbo",
            "temperature": 1,
        },
    }
    #check auth info
    llm_auth = runtime_ctx.get("llm_auth")
    if "GPT" in llm_auth:
        request_data.update({ "llm_auth": llm_auth["GPT"] })
    else:
        raise Exception(f"[request]: llm_auth must be set to agent. use agent.set_llm_auth('GPT', <Your-API-Auth>) to set.")
    #update user customize settings
    cus_llm_url = runtime_ctx.get("llm_url")["GPT"]
    if cus_llm_url:
        request_data.update({ "llm_url": cus_llm_url })
    request_data.update({ "proxy": runtime_ctx.get("proxy") })
    cus_request_options = runtime_ctx.get("request_options")
    if isinstance(cus_request_options, dict):
        for options_name, options_value in runtime_ctx.get("request_options").items():
            request_data["data"].update({ options_name: options_value })
    #get request messages, no transform because standard message style follow GPT API style
    request_data["data"].update({ "messages": runtime_ctx.get("request_messages") })
    return request_data

def request_gpt(request_data):
    url = request_data["llm_url"]
    data = request_data["data"].copy()
    data["stream"] = False
    headers = {
        "Authorization": f"Bearer { request_data['llm_auth'] }",
        "Content-Type": "application/json",
    }
    proxies = request_data["proxy"] if "proxy" in request_data else {}
    return requests.post(url, headers=headers, json=data, proxies=proxies)

def streaming_gpt(request_data):
    url = request_data["llm_url"]
    data = request_data["data"].copy()
    data["stream"] = True
    headers = {
        "Authorization": f"Bearer { request_data['llm_auth'] }",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    proxies = request_data["proxy"] if "proxy" in request_data else {}
    response = requests.post(url, headers=headers, json=data, stream=True ,proxies=proxies)
    return sseclient.SSEClient(response)

def emit_result_gpt(is_streaming, response, listener):
    #emit "done" when get normal request response
    if not is_streaming:
        result = json.loads(response)
        listener.emit("done", result["choices"][0])
    #emit "delta" { "delta": ... } when streaming and emit "done" {"message": ..., finish_reason: ...} when finish
    else:
        buffer = {
            "message": { "role": "", "content": "" },
            "finish_reason": None
        }
        for event in response.events():
            if event.data != "[DONE]":
                delta = json.loads(event.data)["choices"][0]
                listener.emit("delta", delta)
                if delta["delta"]:
                    for key, value in delta["delta"].items():
                        value = buffer["message"][key] + value if key in buffer["message"] else value
                        buffer["message"].update({ key: value })
                if delta["finish_reason"]:
                    buffer["finish_reason"] = delta["finish_reason"]                
            else:
                listener.emit("done", buffer)

'''
MiniMax
'''
def prepare_request_data_minimax(runtime_ctx):
    #default request_data
    request_data = {
        "llm_url": "https://api.minimax.chat/v1/text/chatcompletion",
        "data": {
            "model": "abab5.5-chat",
            "temperature": 1,
        },
    }
    #check auth info
    llm_auth = runtime_ctx.get("llm_auth")
    if "MiniMax" in llm_auth:
        request_data.update({ "llm_auth": llm_auth["MiniMax"] })
    else:
        raise Exception("[request]: llm_auth must be set to agent. use agent.set_llm_auth('MiniMax', <Your-API-Auth>) to set.")
    #update user customize settings
    cus_llm_url = runtime_ctx.get("llm_url")
    if "MiniMax" in cus_llm_url:
        request_data.update({ "llm_url": cus_llm_url["MiniMax"] })
    request_data.update({ "proxy": runtime_ctx.get("proxy") })
    cus_request_options = runtime_ctx.get("request_options")
    if isinstance(cus_request_options, dict):
        for options_name, options_value in runtime_ctx.get("request_options").items():
            request_data["data"].update({ options_name: options_value })
    #get request messages
    request_messages = runtime_ctx.get("request_messages")
    #transform messages format
    prompt = ''
    minimax_user_name = runtime_ctx.get("minimax_user_name")
    minimax_bot_name = runtime_ctx.get("minimax_bot_name")
    final_request_messages = []
    for message in request_messages:
        if message["role"] == "system":
            prompt += f"{ message['content'] }\n"
        else:
            role_mapping = {
                "assistant": "BOT",
                "user": "USER",
            }
            final_request_messages.append({
                "sender_type": role_mapping[message["role"]],
                "text": message["content"]
            })
    request_data["data"].update({
        "messages": final_request_messages,
    })
    if prompt != '':
        request_data["data"].update({
            "prompt": prompt,
            "role_meta": {
                "user_name": minimax_user_name if minimax_user_name else "USER",
                "bot_name": minimax_bot_name if minimax_bot_name else "BOT",
            },
        })
    return request_data

def request_minimax(request_data):
    url = request_data["llm_url"] + "?GroupId=" + request_data["llm_auth"]["group_id"]
    data = request_data["data"].copy()
    data["stream"] = False
    headers = {
        "Authorization": f"Bearer { request_data['llm_auth']['api_key'] }",
        "Content-Type": "application/json",
    }
    proxies = request_data["proxy"] if "proxy" in request_data else {}
    return requests.post(url, headers=headers, json=data, proxies=proxies)

def streaming_minimax(request_data):
    url = request_data["llm_url"] + "?GroupId=" + request_data["llm_auth"]["group_id"]
    data = request_data["data"].copy()
    data["stream"] = True
    data["use_standard_sse"] = True
    headers = {
        "Authorization": f"Bearer { request_data['llm_auth']['api_key'] }",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    proxies = request_data["proxy"] if "proxy" in request_data else {}
    response = requests.post(url, headers=headers, json=data, stream=True ,proxies=proxies)
    return response

def emit_result_minimax(is_streaming, response, listener):
    #emit "done" when get normal request response {}
    if not is_streaming:
        result = json.loads(response)
        minimax_response = result["choices"][0]
        standard_response = {
            "index": minimax_response["index"],
            "message": { "role": "assistant", "content": minimax_response["text"] },
            "finish_reason": minimax_response["finish_reason"],
        }
        listener.emit("done", standard_response)
    #emit "delta" { "delta": ..., "buffer": ... } when streaming and emit "done" {"message": ..., finish_reason: ...} when finish
    else:
        listener.emit("delta", { "delta": { "role": "assistant", "content": "" }, "finish_reason": None })
        for chunk in response.iter_lines():
            if chunk:
                chunk_data = json.loads(chunk.decode('utf-8')[6:])
                delta = chunk_data["choices"][0]
                if "delta" in delta and delta["delta"] != "":
                    listener.emit("delta", { "delta": { "content": delta["delta"] }, "finish_reason": None })
                if "finish_reason" in delta:
                    listener.emit("done", {
                        "message": { "role": "assistant", "content": chunk_data["reply"] },
                        "finish_reason": delta["finish_reason"],
                    })

def update_process(work_node_management):
    result = work_node_management\
        .set_runtime_ctx({
            "llm_name": { "default": "GPT" },
            "request_messages": { "layer": "request", "default": [] }
        })\
        .set_process("prepare_request_data", prepare_request_data_gpt, "GPT")\
        .set_process("request_llm", request_gpt, "GPT")\
        .set_process("streaming_llm", streaming_gpt, "GPT")\
        .set_process("emit_result", emit_result_gpt, "GPT")\
        .set_process("prepare_request_data", prepare_request_data_minimax, "MiniMax")\
        .set_process("request_llm", request_minimax, "MiniMax")\
        .set_process("streaming_llm", streaming_minimax, "MiniMax")\
        .set_process("emit_result", emit_result_minimax, "MiniMax")\
        .set_runtime_ctx({
            "minimax_bot_name": {
                "layer": "agent",
                "alias": { "set": "set_minimax_bot_name" },
            },
            "minimax_user_name": {
                "layer": "agent",
                "alias": { "set": "set_minimax_user_name" },
            },
        })\
        .update()
    return