import streamlit as st
from streamlit_chat import message
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# Initialize session state memory
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

# Initial assistant message
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your career coach. How can I help you grow in your career today?"}
    ]

# 🧠 Define the system prompt (this sets the assistant’s purpose)
system_prompt = """
You are a professional and supportive career coach.
Your goal is to help users advance in their careers by suggesting resources, helping them improve their skills, and providing structured guidance.
You respond with clarity, encouragement, and practical suggestions. Be concise but helpful. Ask clarifying questions if needed.
"""

# 🧠 Set up the chatbot with the system prompt
llm = ChatOpenAI(
    model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
    openai_api_key=st.secrets["TOGETHER_API_KEY"],
    openai_api_base="https://api.together.xyz/v1"
)

conversation = ConversationChain(
    memory=st.session_state.buffer_memory,
    llm=llm,
    verbose=False,
    system_prompt=system_prompt
)

# Streamlit UI
st.title("🧠 Career Growth Assistant")
st.subheader("🎯 Get help improving your skills, finding resources, and advancing your career")

# User input
if prompt := st.chat_input("Ask me anything about your career journey..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate assistant reply
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversation.predict(input=prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
