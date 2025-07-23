import streamlit as st
import requests

# Title and Header
st.set_page_config(page_title="🧠 AI Medical Chatbot", layout="centered")
st.title("🩺 AI Medical Chatbot")
st.markdown("Developed by Shehroz Khan Rind\n\nThis bot acts like a virtual doctor to ask questions and give a probable diagnosis.")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content":
         "You are a virtual AI medical assistant. "
         "Start by greeting the patient and asking about their symptoms. "
         "Based on their replies, ask follow-up questions like duration, severity, location, and history. "
         "After collecting enough information, provide a likely diagnosis and clear recommendation. "
         "Keep asking until you feel confident to proceed to diagnosis. Respond clearly in simple language."}
    ]

# Function to query OpenRouter (Mistral-7B Instruct Free)
def ask_medical_bot(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Display chat history
for chat in st.session_state.chat_history[1:]:
    if chat["role"] == "user":
        st.markdown(f"🧑‍⚕️ **You:** {chat['content']}")
    else:
        st.markdown(f"🤖 **AI Bot:** {chat['content']}")

# Text input
user_input = st.text_input("Enter your reply or symptom here:", key="input")

# On submit
if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("AI is thinking..."):
            ai_response = ask_medical_bot(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.experimental_rerun()

# Clear chat button
if st.button("🔄 Start New Consultation"):
    st.session_state.chat_history = [
        {"role": "system", "content":
         "You are a virtual AI medical assistant. "
         "Start by greeting the patient and asking about their symptoms. "
         "Based on their replies, ask follow-up questions like duration, severity, location, and history. "
         "After collecting enough information, provide a likely diagnosis and clear recommendation. "
         "Keep asking until you feel confident to proceed to diagnosis. Respond clearly in simple language."}
    ]
    st.experimental_rerun()
