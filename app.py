import streamlit as st
from groq import Groq

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="SmartChat AI",
    page_icon="🤖"
)

# -----------------------------
# App title
# -----------------------------
st.title("🤖 SmartChat AI")
st.caption("Your personal GenAI chatbot")

# -----------------------------
# Groq client
# -----------------------------
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# -----------------------------
# System prompt
# -----------------------------
SYSTEM_PROMPT = """
You are SmartChat AI, a helpful, friendly, and knowledgeable AI assistant.

Your instructions:
- Give clear and accurate answers.
- Explain difficult concepts in simple language.
- Be concise unless the user asks for detailed information.
- If you are unsure about something, say so instead of making up information.
"""

# -----------------------------
# Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        st.rerun()

# -----------------------------
# Display chat history
# -----------------------------
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
user_input = st.chat_input("Ask me anything...")

if user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    try:

        # Create an empty assistant message area
        with st.chat_message("assistant"):

            message_placeholder = st.empty()

            full_response = ""

            # Request streaming response
            stream = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=st.session_state.messages,
                stream=True
            )

            # Receive response chunks
            for chunk in stream:

                content = chunk.choices[0].delta.content

                if content:
                    full_response += content

                    message_placeholder.markdown(
                        full_response + "▌"
                    )

            # Display final response
            message_placeholder.markdown(full_response)

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")