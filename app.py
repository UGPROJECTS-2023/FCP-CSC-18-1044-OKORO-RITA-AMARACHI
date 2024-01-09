import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from dotenv import load_dotenv
import os
import random
import string
from jose import jwt

from encrypt import generateKeyPairs, keypairsVal, serializeEncryptionKey, encryptMsg
from LSB import Steganographer

load_dotenv()

AccessKeys = [os.getenv("AccessKey_I")]
SecretKey = os.getenv("SecretKey")
ALGORITHM = os.getenv("ALGORITHM")
encrypted_msg = None
usertoken = None
message = None
img_name = None
img_name_2 = None

def save_image(uploaded_file, name):
    # Open the uploaded image using PIL
    image = Image.open(uploaded_file)

    # Save the image to a file
    image.save(name)
    st.success(f"Image saved successfully as {name}")


def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters_and_digits) for i in range(length))
    return random_string

st.set_page_config(page_title="LSB System", page_icon=":hash:", layout="wide")



st.title('WELCOME')



user_accesKey = st.text_input(label="Enter your access keys to access the App")

if user_accesKey not in AccessKeys:
    st.warning("Please input a valid access key")
    st.stop()


st.warning("access key accepted")

# ---- MAINPAGE ----
st.title(":hash: LSB Steganography With Python")
st.markdown("##")

st.subheader("Hiding a message within any image is easy :point_down:")

lc = """
    <div>
        <h4>
            Generate your encryption keys
        </h4>
        <p> All messages are encrypted before they are hidden!</p>
    </div>
"""

mc = """
    <div>
        <h4> 
            Upload any image 
        </h4>
        <p> add your message; it will be encrypted and hidden in the image </p>
    </div>
"""

rc = """
    <div>
        <h4> 
            Download your image
        </h4>
    </div>
"""


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader(":lock:")
    st.markdown(lc, unsafe_allow_html=True)
with middle_column:
    st.subheader(":bulb:")
    st.markdown(mc, unsafe_allow_html=True)
with right_column:
    st.subheader(":inbox_tray:")
    st.markdown(rc, unsafe_allow_html=True)


genKeys = st.button("generate your encryption keys :key:", help="use this button to generate encryption keys")

if genKeys:
    privateKey, publicKey = keypairsVal()
    usertoken = jwt.encode({"id": "1o1oo330"}, SecretKey, algorithm=ALGORITHM)
    st.session_state[f'PRIV-{usertoken}'] = privateKey
    st.session_state[f'PUB-{usertoken}'] = publicKey
    st.write(f"Your encryption token is: {usertoken}")

if usertoken:
    message = st.text_input(label="Enter your message here")

    print(message)
    if message:
        _e = serializeEncryptionKey(keystr=st.session_state[f'PRIV-{usertoken}'].encode('utf-8'))

        encrypted_msg = encryptMsg(msg=message.encode('utf-8'), public_key=_e.public_key())


        input_file = st.file_uploader(label="Select Image", type=["jpg", "png", "jpeg"])

        if input_file is not None:
            img_name = f"{generate_random_string(12)}.jpg"
            save_image(uploaded_file=input_file, name=img_name)
            
            if img_name:     
                s = Steganographer(imgpath=img_name, message=encrypted_msg)
                s.open_image()
                msg_bits = s.decode_msg()
                s.reshape_img(msg_bits=msg_bits)

                original_img, encoded_img = st.columns(2)
                with original_img:
                    st.subheader("Original Image")
                    # Display the uploaded image
                    st.image(input_file, caption="Uploaded Image", use_column_width=True)

                with encoded_img:
                    st.subheader("Encoded Img")
                    enc_img = Image.fromarray(s.simage)
                    st.image(enc_img)

                    img_name_2 = f"{generate_random_string(12)}.jpg"
                    enc_img.save(img_name_2)
            else:
                print("no image name")

            if img_name_2:
                with open(img_name_2, "rb") as file:
                    btn = st.download_button(
                            label="Download encoded image",
                            data=file,
                            file_name=img_name_2,
                            mime="image/png"
                        )
            else: print("no image_2")
        else:
            print("input file is none")
    else:
        st.warning("Please provide a message to continute")
else:
    st.warning("Please generate your encryption keys to proceed")
    

