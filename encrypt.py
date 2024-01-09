from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding



def generateKeyPairs():
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    # Serialize public key
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key, public_key, pem


def serializeEncryptionKey(filename: str):

    private_key = None
    
    # Load private key from PEM file
    with open(filename, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # Provide the password if the key is encrypted
            backend=default_backend()
        )
    return private_key

def serializePubEncryptionKey(filename: str):

    public_key = None
    
    # Load private key from PEM file
    with open(filename, 'rb') as key_file:
        private_key = serialization.load_pem_public_key(
            key_file.read(),
            password=None,  # Provide the password if the key is encrypted
            backend=default_backend()
        )
    return public_key


def encryptMsg(msg: str, public_key: rsa.RSAPublicKey):
    
    # Encrypt using the public key
    plaintext_message = bytes(msg)
    ciphertext = public_key.encrypt(
        plaintext_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return str(ciphertext)

def decryptMsg(ciphertext: bytes, private_key: rsa.RSAPrivateKey):
    # Decrypt using the private key
    decrypted_message = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_message



def keypairsVal():
    privateKey, _,  pem = generateKeyPairs()

    privateKeyVal = privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    pem_str = pem.decode('utf-8')


    return privateKey, privateKeyVal, pem_str

ky = b'''
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdesGGIpR27Pzt
7BvOn8ji8tEnoLvBxWQoUyxdFYIGlXwAiB2I8wawMOTzaarsYWStpJ4ZuAJGqLla
76q7juMKqca2TbheH848X4XcSibc8gM+nMSbNg18/wP5TdUprIRVaSfGlJjDbnrm
rzEv5rEDE4Fp1bNEiIyptazMspH/wWf4hCcfR5H93BXVH6ABG1yqDlgDDOhC6bZb
N3LMtOuAB4htHV6QAQNO1rwWr/qUi2VjJr+jy97EDBnCKXqUkg1ZW/xfRu2hfAgE
AIOx2LPaR2yr+ltkme4A3cbp1f4MTbnAY81NLysMhMIRBzsyyKICxU29iLz+yu19
kNdQjpHNAgMBAAECggEABQBSXRGEEt175Y0gukiAzL8BaCIb/w9nGuYT+/DO7FPw
WDlPwXsBCgoY0KeDx3YLCH4N4gCMsfRxzogwrTw1zFo6oVeJNL61110BQfm+OjjF
ZEZTnXTzVguTSLucEB1r0SVByiC1/p7nmvk9X/686GgaLWOdXzPRo8zNQW2lDVuT
pobUCcQWbC7ADXXJoFZoAzEqOl8KD3jxK7RtlASXSu1mdkaB/B0aPzhTYq796grO
Ign99Wt3ECUkwb+Cl2/wVFcssIJoyeQMr9Xuu3TEELCuaPY7pgcrDnjEYdM4O9pj
x0UWtxjEBzXTCqQyrTjvM0WHYN4yqaJ+HqTlovXCUQKBgQDN2g/ckqUM82dTKsh+
YRQV/NO8PIt3w5rS+92J9v9ocjqgl8bjcQwL65Iy84EYlv7+1xtx40w9U4RyHY/I
6NZqhKE/2LEB8g8QJqaXvjogltRa2eE7Xl/C3u3NLv4Ymg8j6MaPfU639HYouvwK
rE5fMEHYJdtpodcpXZlRfyfOnwKBgQDD1/Vepd/+25KUOm6IBq/SiK07Zuc6j6ql
yzqXmelBg6EchDQsaGBCIYQsmcnzaTTN7POGPUobqmVEuY8oCt5EqX7ALCt9myaf
z+jGjay851ronoYbunEjYxDqfLy/WVJ5bjihf+jrzI3peTuSF9PAa0T6dq8F+hVq
cUQ9L0hEEwKBgHUkxegA77o5/a+/Zg89UX/du+SgE8IY509vkzgC/n/CmYhwNveR
iohyC2XBWtLSgtQlN3INJoKzt2h1WDC+B97gER9TQg/YXygSxrUNxOhszPXSjbEK
WLZ9xJgCSQlZCoql2fEoHxbiICe3mNy+B29199J4YK9xMQ9SO4C8OrwDAoGAHh51
ZwP9qfVc2p0N6K+WlLteYPdXcmMr7GmP7kbGX8P9oCQY3geDXkhHSpCwRVYVv+HE
Jg4A+rY+8s3S3WamfkrO6oEggyW8T/Gqq/aX7UlrasEOgO8wfS+8J0Pdx1PWYkR4
QyYnzTPdU13IspQlhb85kYd1LWcjqgYXZ42BAK8CgYEAv5lvyNrjHdN7tpm2Y4U2
MXwsWbMR3j2bvwl0R3an8umRn3THD7y6Uk2AFezU7BQmTLk888B6ehq5XkdzxRWs
GToV87okMIhayK6b6t1lu2X0/XOQgPW1xHk1J8bEdnCw1KS90taBYQzflv269IEN
tQ1gaVvZoQ0wSSKHXidu6Ig=
-----END PRIVATE KEY-----
'''

#print(serializeEncryptionKey(keystr=ky))

'''
    generate encryption keys
    upload the image
    add your message
    recieve encoded image


    upload encoded image
    recieve encrypted message
    decrypt message with private key
'''