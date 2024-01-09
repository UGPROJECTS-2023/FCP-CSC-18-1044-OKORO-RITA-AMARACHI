from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


class Steganographer():

    def __init__(self, imgpath:str, message:str) -> None:
       self.imgpath = imgpath
       self.message = message

    def open_image(self):
        self.image = np.array(Image.open(self.imgpath))
        self.img_W, self.img_H, self.img_B = self.image.shape
        return self.image

    def decode_msg(self):
        self.message += "[END]"
        self.message = self.message.encode("ascii")
        message_bits = ''.join([format(i, '08b') for i in self.message])
        return message_bits

    def reshape_img(self, msg_bits):
        self.image = self.image.flatten()
        for idx, bit in enumerate(msg_bits):
            val = self.image[idx]
            val = bin(val)
            val = val[:-1] + bit
            self.image[idx] = int(val, 2)

        self.image = self.image.reshape((self.img_W, self.img_H, self.img_B))


    def decode_img(self):
        msg = ""
        idx = 0
        self.image = self.image.flatten()

        while msg[-5:] != '[END]':
            bits = [bin(i)[-1] for i in self.image[idx:idx+8]]
            bits = "".join(bits)
            msg += chr(int(bits, 2))
            idx += 8
            if idx > self.image.shape[0]:
                print("There is no hidden message")
                break    
        return msg


    def decodE_img_ext(self, img: Image.Image):
        msg = ""
        idx = 0
        img = np.array(img)
        img = img.flatten()        
        while msg[-5:] != '[END]':
            bits = [bin(i)[-1] for i in img[idx:idx+8]]
            bits = "".join(bits)
            msg += chr(int(bits, 2))
            idx += 8
            if idx > img.shape[0]:
                print("There is no hidden message")
                break    
        return msg

    @property
    def simage(self):
        return self.image
        

#s = Steganographer(imgpath="images (2).jpeg", message="first is to initial the steganographer")
#s.open_image()
#msg_bits = s.decode_msg()
#print(msg_bits)
#s.reshape_img(msg_bits=msg_bits)

#coded_image = Image.fromarray(s.simage)
#coded_image.show()  #save the image
#print(s.decode_img())

#i = Image.open("/tmp/tmpj6xmw3qv.PNG")
#print(s.decodE_img_ext(img=i))
