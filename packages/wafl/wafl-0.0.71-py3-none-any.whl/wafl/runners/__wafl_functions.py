from wafl.exceptions import CloseConversation


async def close_conversation(inference, policy, task_memory):
    raise CloseConversation()
