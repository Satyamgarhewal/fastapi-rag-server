import getpass
import os
from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model = "gpt-4o-mini")
workflow = StateGraph(state_schema = MessagesState)

def langchain_rag(state: MessagesState, retrieved_docs=None):
    try:
        system_prompt = (
            "You are a helpful assistant.\n"
            "Answer all the questions based on the retrieved documents.\n"
            "The provided chat history includes a summary of the earlier conversation."
        )

        system_message = SystemMessage(content=system_prompt)
        message_history = state["messages"][:-1]

        # If retrieved_docs are provided, add them as context
        if retrieved_docs:
            context_message = SystemMessage(content=f"Context documents: {retrieved_docs}")
            base_messages = [system_message, context_message]
        else:
            base_messages = [system_message]

        if len(message_history) >= 10:
            last_human_message = state["messages"][:-1]
            summary_prompt = (
                "Distill the above chat messages into a single summary message. "
                "Include as many specific details as you can."
            )
            summary_message = model.invoke(
                message_history + [HumanMessage(content=summary_prompt)]
            )

            delete_messages = [RemoveMessage(id=m.id) for m in state["messages"]]
            human_message = HumanMessage(content=last_human_message.content)
            response = model.invoke(base_messages + [summary_message, human_message])
            message_updates = [summary_message, human_message, response] + delete_messages
        else:
            message_updates = model.invoke(base_messages + state["messages"])

        return {"messages": message_updates}
    except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))
    
workflow.add_node("model", langchain_rag)
workflow.add_edge(START, "model")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)