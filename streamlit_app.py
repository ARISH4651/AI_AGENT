import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
import os

# Load environment variables
load_dotenv()

# Create agent (same config as agent.py)
# NOTE: The agent setup should ideally be outside the main script run block 
# for efficiency, but here it's fine for a simple app.
agent = create_agent(
    model="groq:llama-3.1-8b-instant",
    tools={},
    system_prompt=(
        "You are a helpful chat assistant. Be clear, concise and polite. "
        "Understand the user's needs and provide accurate information. "
        "Stay professional and safe."
    ),
)

st.set_page_config(page_title="Chat Assistant", layout="centered")
st.title("Chat Assistant")

# Initialize chat history in session state
if "history" not in st.session_state:
    # history stores messages in the format expected by the agent:
    # [{"role": "user", "content": "..."}]
    st.session_state.history = []

# --- Input Form ---
# Use a key on the text_input for better state management if needed, 
# but your current form/clear_on_submit logic is okay.

# The form is now just to group the input and button
with st.form("input_form", clear_on_submit=True):
    user_input = st.text_input("You:", key="user_input_text") # Added a key
    submitted = st.form_submit_button("Send")

# --- Agent Invocation and History Update ---
if submitted and user_input:
    # 1. Add user message to history
    st.session_state.history.append({"role": "user", "content": user_input})
    
    # 2. Invoke agent with **FULL** history (for context)
    try:
        # Pass the ENTIRE history list to the agent for context
        result = agent.invoke({"messages": st.session_state.history}) 
        
        # The agent's response is the content of the last message in the result's messages list
        response = result["messages"][-1].content 
    except Exception as e:
        # Check if GROQ_API_KEY is missing or invalid if an error occurs
        response = f"Error during agent invocation: {e}"

    # 3. Add assistant response to history
    st.session_state.history.append({"role": "assistant", "content": response})

# --- Render Chat History ---
# Use a single container for better display control, and crucially, 
# use **msg["content"]** instead of msg["response"]
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        # **FIXED:** Changed msg["response"] to msg["content"]
        st.markdown(f"**Assistant:** {msg['content']}")

st.markdown("---")
st.caption("Powered by Arish")