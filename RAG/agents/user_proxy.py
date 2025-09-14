from autogen import UserProxyAgent

def UserProxy():
    return UserProxyAgent(name="User", human_input_mode="NEVER", is_termination_msg=lambda x: x.get("content", "").endswith("FINAL"))
