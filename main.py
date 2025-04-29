import streamlit as st
import requests
import json
import time

# === CONFIGURATION ===

# Get your API key securely from Streamlit secrets
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL = "openai/gpt-3.5-turbo"

# === HARVEST FUNCTION ===

def extract_value_from_chaos(raw_text):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You're an AI that extracts useful insights from noisy, chaotic, or vague data."},
            {"role": "user", "content": f"Here is the data: {raw_text}. What valuable insight can you extract?"}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"[Error from OpenRouter: {response.status_code} - {response.text}]"

# === Streamlit App ===

st.title("🧠 Mind Miner — Extract Wisdom from Chaos")
st.markdown("This tool helps you turn messy thoughts, random ideas, or chaotic situations into clear, valuable insights using AI.")

chaotic_input = st.text_area("Enter your chaotic text, notes, or confusion below:", height=200)

if st.button("🔍 Harvest Insight"):
    if not chaotic_input.strip():
        st.warning("Please enter something to analyze.")
    else:
        with st.spinner("Extracting insight using GPT..."):
            result = extract_value_from_chaos(chaotic_input)
            st.success("✅ Insight Extracted!")
            st.write(result)

        # Save to local file
        with open("insight_log.json", "a") as f:
            f.write(json.dumps({
                "input": chaotic_input,
                "output": result,
                "timestamp": time.ctime()
            }) + "\n")
