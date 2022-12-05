# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
import math

def bin_message(message): #gizlenecek mesaj icin gerekli islemler
    message += "final" #sonlandirici anahtar kelimesi
    b_message = ''.join([format(ord(i), "08b") for i in message])
    return b_message

def img_mode(img):
    n = 3
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    return n

def Encode(src, message, dest, x, a):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    n = img_mode(img)
    total_pixels = array.size//n

    b_message = bin_message(message)
    len_b_message = len(b_message)

    selected_pixels = random_sin(len_b_message/3, total_pixels, x, a)#sinus formulune gore rastgele pixeller secilir ve diziye atanir

    if len_b_message > total_pixels:
        print("Bu veri icin daha buyuk boyutlu resim gereklidir!!")

    else:
        index=0
        for p in selected_pixels:
            for q in range(0, 3):
                if index < len_b_message:
                    array[p][q] = int(bin(array[p][q])[:-1]+b_message[index], 2)
                    index += 1

    array=array.reshape(height, width, n)
    enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    enc_img.save(dest)
    print("Veri gizlendi")


def hidden_bit(selected_pixels, array):
    hidden_bits = ""
    for p in selected_pixels:
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])
    return hidden_bits
    

def Decode(src, x, a):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    n = img_mode(img)
    total_pixels = array.size//n

    selected_pixels = random_sin(total_pixels/10, total_pixels, x, a)#sinus formulune gore rastgele pixeller secilir ve diziye atanir
    hidden_bits = hidden_bit(selected_pixels,array) # secili olan butun pixellerin son biti alinir ve birlestirilir
    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)] # 8 li gruplara ayrilir

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "final":
            break
        else:
            message += chr(int(hidden_bits[i], 2))

    if "final" in message:
        print("Gizli mesaj:", message[:-5])
    else:
        print("Gizli mesaj bulunamadi")


def random_sin(len_b_message, total_pixel, x, a):
    k = 0.93 # k 0 ile 1 araliginda secilmelidir
    #x 0 ile 1 araliginda secilmelidir
    array = []

    i=0
    while(i < len_b_message ): # gizlenecek metnin uzunlugu
        result = k * math.sin(a*x)
        x = result
        value = int(abs(x)*total_pixel) # resmin olcusune gore carpim degeri belirlenir

        if(value not in array): # ayni index daha once alinmis mi kontrol edilir
            array.append(value)
            i+=1  
        #else:
            #print("ayni pixel degeri::",value)

    return array

Encode('image.png','gizli metin ornek','new_image.png', 0.8, 38)
Decode('new_image.png', 0.8, 38)