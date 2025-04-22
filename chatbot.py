import streamlit as st
from streamlit_chat import message
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from uuid import uuid4

# Initialize session ID for message memory
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

# Initialize message memory
memory = ConversationBufferWindowMemory(k=3, return_messages=True)

# Set up the LLM
llm = ChatOpenAI(
    model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
    openai_api_key=st.secrets["TOGETHER_API_KEY"],
    openai_api_base="https://api.together.xyz/v1"
)

# System prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a supportive career coach who helps users improve their skills, find resources, and grow professionally."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Chain with memory
chain = prompt | llm
chat_chain = RunnableWithMessageHistory(
    chain,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="history"
)

# Streamlit UI
st.title("🧠 Career Coach Chatbot")

# Initial assistant message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I’m your career coach. How can I help you today?"}
    ]

# User input
if prompt_text := st.chat_input("Ask me about your career journey..."):
    st.session_state.messages.append({"role": "user", "content": prompt_text})

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Generate assistant reply
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = chat_chain.invoke(
                {"input": prompt_text},
                config={"configurable": {"session_id": st.session_state.session_id}}
            )
            st.write(result.content)
            st.session_state.messages.append({"role": "assistant", "content": result.content})
