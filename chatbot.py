
import streamlit as st
import requests

# Set your Together API key here
TOGETHER_API_KEY = "f4816e6d5c5698ba7ae4a710536804c3070ce8a823e87f8b7dad5cbf39d0ad56"

# System prompt for the career coach bot
system_prompt = """
You are a friendly and knowledgeable career coach. 
Your job is to guide users in their professional journey. 
Provide personalized advice, helpful resources (with links), and actionable tips for career advancement. 
Encourage users and use a positive tone. 
If asked for resources, include useful websites, books, or course links (e.g., Coursera, edX, Khan Academy).
"""

# Initialize chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# App UI
st.set_page_config(page_title="Career Coach Chatbot", page_icon="🎯")
st.title("🎯 Career Coach Chatbot")
st.write("Ask me anything about your career. I can help with job roles, learning resources, and professional growth tips.")

# User input
user_input = st.text_input("You:", "")

# Send to Together API
def query_together(messages):
    response = requests.post(
        "https://api.together.xyz/inference",
        headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
        json={
            "model": "meta-llama/Llama-2-70b-chat-hf",
            "messages": messages,
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 512,
            "stop": None,
            "stream": False,
        },
    )
    response.raise_for_status()
    return response.json()["output"]["choices"][0]["message"]["content"]

# Handle user input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        bot_response = query_together(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system prompt
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Career Coach:** {msg['content']}")
