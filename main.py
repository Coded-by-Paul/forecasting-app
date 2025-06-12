import streamlit as st
import openai
import os
import pandas as pd
from io import BytesIO

# Must be the first Streamlit call
st.set_page_config(page_title="Batch Forecasting with GPT-3.5")

# Background color
st.markdown("""
    <style>
    .stApp {
        background-color: #009fe3;
    }
    </style>
""", unsafe_allow_html=True)

# OpenAI client setup
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Display logo at the top-left corner above the title
st.image("logo.jpg", width=120)  # You can adjust the width

st.title("AMI B.V. Forecasting with GPT-3.5 fine-tuned")

uploaded_file = st.file_uploader("Upload an Excel file with prompts in Column A and the title 'Prompts' in A1", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if df.shape[1] >= 1:
        st.success(f"File uploaded successfully. Found {len(df)} prompts.")

        if st.button("Run Forecasting"):
            with st.spinner("Sending prompts to GPT-3.5 Turbo..."):
                results = []
                for prompt in df.iloc[:, 0].astype(str):
                    try:
                        response = client.chat.completions.create(
                            model="ft:gpt-3.5-turbo-0125:bachelor-project::BP4Z7c6r",  # Replace with your model ID
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0
                        )
                        results.append(response.choices[0].message.content)
                    except Exception as e:
                        results.append(f"ERROR: {e}")

                df["Response"] = results
                st.success("Done! See results below.")
                st.dataframe(df)

                # Prepare download
                output = BytesIO()
                df.to_excel(output, index=False, engine='openpyxl')
                output.seek(0)

                st.download_button(
                    label="Download Results as Excel",
                    data=output,
                    file_name="forecast_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.error("No columns found in uploaded file.")
