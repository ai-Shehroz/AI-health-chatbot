import streamlit as st
import requests

st.set_page_config(page_title="🩺 AI Health Chatbot", layout="centered")

st.markdown("<h1 style='text-align: center;'>🤖 AI Medical Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>I will ask relevant medical questions, analyze your responses, and suggest possible diagnoses and care tips.</p>", unsafe_allow_html=True)

API_KEY = st.secrets["OPENROUTER_API_KEY"]
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

messages = st.session_state.get("messages", [])

# Initial system message
if not messages:
    messages.append({"role": "system", "content": (
        "You are an AI medical assistant. "
        "Begin by asking the user about symptoms, age, duration, and any other necessary details. "
        "Once enough information is gathered, provide a preliminary suggestion (not a diagnosis) and recommend next steps. "
        "Be concise, medically appropriate, and use simple language."
    )})

# Display chat
for msg in messages[1:]:  # skip system message
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your symptoms or questions..."):
    messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    try:
        payload = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": messages,
        }
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"]

        messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").markdown(reply)

    except Exception as e:
        st.error(f"Error: {e}")

st.session_state["messages"] = messages
