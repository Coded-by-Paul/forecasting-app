import streamlit as st
import openai

st.set_page_config(page_title="Forecasting App with GPT-3.5")

st.title("Forecasting with Your Fine-Tuned GPT-3.5 Turbo")

openai.api_key = "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"  # ⛔ Replace with your real API key

user_input = st.text_input("Enter your input (e.g. product and monthly data):")

if st.button("Generate Forecast"):
    if user_input:
        with st.spinner("Generating forecast..."):
            response = openai.ChatCompletion.create(
                model="ft:gpt-3.5-turbo-0125:bachelor-project::BP4Z7c6r",  # ⛔ Replace with your fine-tuned model name
                messages=[
                    {"role": "user", "content": user_input}
                ],
                temperature=0  # ✅ Deterministic output
            )
            st.markdown("### 📈 Forecast Result:")
            st.success(response['choices'][0]['message']['content'])
