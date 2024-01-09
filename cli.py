import typer
from jose import jwt
import os
import string
import random
from datetime import datetime, timedelta
from PIL import Image
from dotenv import load_dotenv

from encrypt import generateKeyPairs, keypairsVal, serializeEncryptionKey, encryptMsg, decryptMsg
from LSB import Steganographer

load_dotenv()

app = typer.Typer()


AccessKeys = [os.getenv("AccessKey_I")]
SecretKey = os.getenv("SecretKey")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])


def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters_and_digits) for i in range(length))
    return random_string



@app.command()
def hello(name: str):
    print(f"Hello {name}")





@app.command()
def generate_encryption_key():
        print("Generating Encryption Key Pairs")

        p_key, privateKey, publicKey = keypairsVal()

        print(privateKey)
        print(publicKey)

        print("make sure to store these credentials in a safe place")

                # Write PEM data to the file
        with open(f"{generate_random_string(12)}.pem", 'wb') as pem_file:
            pem_file.write(privateKey.encode('utf-8'))
            pem_file.write("\n".encode('utf-8'))
            pem_file.write(publicKey.encode('utf-8'))



@app.command()
def encode_picture(path: str, filename: str = typer.Option(..., prompt="Enter your private key file name")):
    
    msg = input("enter your message: ")

    print("encoding.................")

 
    _e = serializeEncryptionKey(filename=filename)

    encrypted_msg = encryptMsg(msg=msg.encode('utf-8'), public_key=_e.public_key())

    print(encrypted_msg)
    print("encoding..................")

    print(path)
    pth = os.getcwd()
    imgpth = os.path.join(pth, path)
    s = Steganographer(imgpath=imgpth, message=encrypted_msg)

    s.open_image()
    msg_bits = s.decode_msg()
    s.reshape_img(msg_bits=msg_bits)

    coded_image = Image.fromarray(s.simage)
    coded_image.show()  #save the image

        
    basepath = input("enter the path you want your encode image saved: ")

    img_name_2 = f"{generate_random_string(12)}.jpg"
    imgpath = os.path.join(basepath, img_name_2)
    coded_image.save(imgpath)
    
    print("image has been encoded and saved successfully!")


@app.command()
def decode_picture(path: str, filename: str = typer.Option(..., prompt="Enter your private key file name")):
    s = Steganographer(imgpath=path, message="encrypted_msg")

    img = Image.open(path)

    _e = serializeEncryptionKey(filename=filename)
    print(_e)

    strg = s.decodE_img_ext(img=img)


    """   print(strg)
        decrypted_msg = decryptMsg(strg.encode('utf-8'), _e)

        print(decrypted_msg)
    """

if __name__ == "__main__":
    app()