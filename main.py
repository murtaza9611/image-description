import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests

load_dotenv()
OPENAI_API_KEY = st.text_input("OPENAI API KEY")
IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    response = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": IMGBB_API_KEY},
        files={"image": bytes_data},
    )

    if response.status_code == 200:
        image_url = response.json()["data"]["url"]

        client = OpenAI(api_key=OPENAI_API_KEY)

        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Provide a detailed description of the image provided."},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url},
                            },
                        ],
                    }
                ],
            )

            st.title("Image Description:")
            st.write(completion.choices[0].message.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Failed to upload the image. Please try again.")
