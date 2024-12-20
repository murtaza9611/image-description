import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_KEY")
IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY")

st.title("Computer Vision for Diagnostic of Medical Images:hospital:")
st.sidebar.header(":red[Please Upload an Image:]")
uploaded_file = st.sidebar. file_uploader("")
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
                            {"type": "text", "text": "Provide a concise and accurate description of the image provided. You have to give response in descriptive format rather than list."},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url},
                            },
                        ],
                    }
                ],
            )

            st.header(":green[Image Description:]")
            container = st.container(border=True)
            container.write(completion.choices[0].message.content)
            # st.write(completion.choices[0].message.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Failed to upload the image. Please try again.")
