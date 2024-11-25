from typing import List
import pydantic as pyd2
from langchain_community.chat_models import ChatClovaX
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser

import streamlit as st

llm = ChatClovaX(model="HCX-DASH-001")

parser = JsonOutputParser()
format_instruction = parser.get_format_instructions()

class Turn(pyd2.BaseModel):
    role: str = pyd2.Field(description="role")
    content: str = pyd2.Field(description="content")

class Messages(pyd2.BaseModel):
    messages: List[Turn] = pyd2.Field(description="message", default=[])

type_to_msg_class_map = {
        "system":  SystemMessage,
        "user":  HumanMessage,
        "assistant":  AIMessage,
        }

def chat(messages):
    messages_lc = []
    for msg in messages:
        msg_class = type_to_msg_class_map[msg["role"]]
        msg_lc = msg_class(content=msg["content"])

        messages_lc.append(msg_lc)
        
    resp = llm.invoke(messages_lc)
    return {"role": "assistant", "content": resp.content}



def main():
    st.title("Woo, Sangmin")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    tmpt= st.chat_input("Say something")
    if tmpt:
        user_turn = {"role": "user", "content": str(tmpt)}
        st.session_state.messages.append(user_turn)
        resp = chat(st.session_state.messages)
        st.session_state.messages.append(resp)

        print(st.session_state.messages)
        for msg in st.session_state.messages:
            if(msg["role"]=="user"):
                with st.chat_message("user"):
                    st.write(msg['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(msg['content'])

    
if __name__=="__main__":
    main()
