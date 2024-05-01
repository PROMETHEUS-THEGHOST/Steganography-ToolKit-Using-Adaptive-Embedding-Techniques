import numpy as np
import pandas as pand
import os
import cv2
import wave
from matplotlib import pyplot as plt

def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S, n):
    i = 0
    j = 0
    key = []
    while n > 0:
        n = n - 1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        key.append(K)
    return key

def preparing_key_array(s):
    return [ord(c) for c in s]

def RC4_encrypt(text, key):
    key = preparing_key_array(key)
    S = KSA(key)
    keystream = PRGA(S, len(text))
    keystream = bytes(keystream)
    encrypted = bytes([c ^ k for c, k in zip(text, keystream)])
    return encrypted

def RC4_decrypt(encrypted_text, key):
    S = KSA(key)
    key = preparing_key_array(key)
    keystream = PRGA(S, len(encrypted_text))
    keystream = bytes(keystream)
    decrypted = bytes([c ^ k for c, k in zip(encrypted_text, keystream)])
    return decrypted

def encode_txt_data():
    count2 = 0
    file1 = open("C://Users//HP//Steganography-ToolKit-Using-Adaptive-Embedding-Techniques//covertext_sample.txt", "r")
    for line in file1:
        for word in line.split():
            count2 = count2 + 1
    file1.close()
    bt = int(count2)
    print("Maximum number of words that can be inserted:", int(bt / 6))
    text1 = input("Enter data to be encoded: ")
    key = input("Enter the key for encryption: ")
    encrypted_text = RC4_encrypt(text1.encode(), key)
    l = len(encrypted_text)
    if l <= bt:
        print("\nInputted message can be hidden in the cover file\n")
        txt_encode(encrypted_text, key)
    else:
        print("\nString is too big, please reduce string size")
        encode_txt_data()

def txt_encode(text, key):
    text = str(text, 'utf-8')  # Convert bytes to string
    l = len(text)
    i = 0
    add = ''
    while i < l:
        t = ord(text[i])
        if 32 <= t <= 64:
            t1 = t + 48
            t2 = t1 ^ 170       # 170: 10101010
            res = bin(t2)[2:].zfill(8)
            add += "0011" + res
        
        else:
            t1 = t - 48
            t2 = t1 ^ 170
            res = bin(t2)[2:].zfill(8)
            add += "0110" + res
        i += 1
    res1 = add + "111111111111"
    print("The string after binary conversion applying all the transformations:", res1)   
    length = len(res1)
    print("Length of binary after conversion:", length)
    HM_SK = ""
    ZWC = {"00": "\u200C", "01": "\u202C", "11": "\u202D", "10": "\u200E"}      
    file1 = open("C://Users//HP//Steganography-ToolKit-Using-Adaptive-Embedding-Techniques//covertext_sample.txt", "r+")
    nameoffile = input("Enter the name of the Stego file after Encoding (with extension): ")
    file3 = open(nameoffile, "w+", encoding="utf-8")
    word = []
    for line in file1: 
        word += line.split()
    i = 0
    while i < len(res1):  
        s = word[int(i/12)]
        j = 0
        x = ""
        HM_SK = ""
        while j < 12:
            x = res1[j + i] + res1[i + j + 1]
            HM_SK += ZWC[x]
            j += 2
        s1 = s + HM_SK
        file3.write(s1)
        file3.write(" ")
        i += 12
    t = int(len(res1) / 12)     
    while t < len(word): 
        file3.write(word[t])
        file3.write(" ")
        t += 1
    file3.close()  
    file1.close()
    print("\nStego file has been successfully generated.")

def decode_txt_data(key):  # Pass 'key' as a parameter
    ZWC_reverse = {"\u200C": "00", "\u202C": "01", "\u202D": "11", "\u200E": "10"}
    stego = input("\nPlease enter the stego file name (with extension) to decode the message: ")
    file4 = open(stego, "r", encoding="utf-8")
    temp = ''
    for line in file4:
        for words in line.split():
            T1 = words
            binary_extract = ""
            for letter in T1:
                if letter in ZWC_reverse:
                    binary_extract += ZWC_reverse[letter]
            if binary_extract == "111111111111":
                break
            else:
                temp += binary_extract
    print("\nEncrypted message presented in code bits:", temp)
    lengthd = len(temp)
    print("\nLength of encoded bits:", lengthd)
    i = 0
    a = 0
    b = 4
    c = 4
    d = 12
    final = ''
    while i < len(temp):
        t3 = temp[a:b]
        a += 12
        b += 12
        i += 12
        t4 = temp[c:d]
        c += 12
        d += 12
        if t3 == '0110':
            decrypted_data = RC4_decrypt(int(t4, 2).to_bytes((len(t4) + 7) // 8, byteorder='big'), key) # Decrypt binary to bytes
            final += decrypted_data.decode('utf-8', 'ignore')  # Decode with 'ignore' error handling
        elif t3 == '0011':
            decrypted_data = RC4_decrypt(int(t4, 2).to_bytes((len(t4) + 7) // 8, byteorder='big'), key) # Decrypt binary to bytes
            final += decrypted_data.decode('utf-8', 'ignore')  # Decode with 'ignore' error handling
    print("\nMessage after decoding from the stego file:", final)
def txt_steg():
    while True:
        print("\n\t\tTEXT STEGANOGRAPHY OPERATIONS")
        print("1. Encode the Text message")
        print("2. Decode the Text message")
        print("3. Exit")
        choice1 = int(input("Enter the Choice: "))
        if choice1 == 1:
            encode_txt_data()
        elif choice1 == 2:
            key = input("Enter the key for decryption: ")
            decode_txt_data(key)  # Pass 'key' to decode_txt_data function
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")

def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S, n):
    i = 0
    j = 0
    key = []
    while n > 0:
        n = n - 1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        key.append(K)
    return key

def msgtobinary(msg):
    if type(msg) == str:
        result= ''.join([ format(ord(i), "08b") for i in msg ])
    
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result= [ format(i, "08b") for i in msg ]
    
    elif type(msg) == int or type(msg) == np.uint8:
        result=format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    
    return result

def preparing_key_array(key):
    if isinstance(key, int):
        return [key] * 256
    elif isinstance(key, str):
        return [ord(c) for c in key]
    else:
        raise TypeError("Key type not supported")

def RC4_encrypt(data, key):
    key = preparing_key_array(key)
    return data # Placeholder, replace with actual encryption logic

def RC4_decrypt(data, key):
    key = preparing_key_array(key)
    return data # Placeholder, replace with actual decryption logic

def encode_img_data(img):
    data=input("\nEnter the data to be Encoded in Image :")    
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')
  
    nameoffile = input("\nEnter the name of the New Image (Stego Image) after Encoding(with extension):")
    
    no_of_bytes=(img.shape[0] * img.shape[1] * 3) // 8
    
    print("\t\nMaximum bytes to encode in Image :", no_of_bytes)
    
    if(len(data)>no_of_bytes):
        raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")
    
    data +='*^*^*'    
    
    binary_data=msgtobinary(data)
    print("\n")
    print(binary_data)
    length_data=len(binary_data)
    
    print("\nThe Length of Binary data",length_data)
    
    index_data = 0
    
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
    cv2.imwrite(nameoffile,img)
    print("\nEncoded the data successfully in the Image and the image is successfully saved with name ",nameoffile)

def decode_img_data(img):
    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*": 
                    print("\n\nThe Encoded data which was hidden in the Image was :--  ",decoded_data[:-5])
                    return 

def img_steg():
    while True:
        print("\n\t\tIMAGE STEGANOGRAPHY OPERATIONS")
        print("1. Encode the Text message")
        print("2. Decode the Text message")
        print("3. Exit")
        choice1 = int(input("Enter the Choice: "))
        if choice1 == 1:
            key = input("Enter the key for encryption: ")  # Prompt the user to enter the key as a string
            image = cv2.imread("C://Users//HP//Steganography-ToolKit-Using-Adaptive-Embedding-Techniques//coverimage_sample.png")
            encrypted_image = RC4_encrypt(image, key)  # Pass the key as a string
            encode_img_data(encrypted_image)
        elif choice1 == 2:
            image1 = cv2.imread(input("Enter the Image you need to Decode to get the Secret message :  "))
            key = input("Enter the key for decryption: ")  # Prompt the user to enter the key as a string
            decrypted_image = RC4_decrypt(image1, key)  # Pass the key as a string
            decode_img_data(decrypted_image)
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")

def encode_aud_data():
    import wave

    nameoffile=input("Enter name of the file (with extension) :- ")
    song = wave.open(nameoffile, mode='rb')

    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    data = input("\nEnter the secret message :- ")

    res = ''.join(format(i, '08b') for i in bytearray(data, encoding ='utf-8'))     
    print("\nThe string after binary conversion :- " + (res))   
    length = len(res)
    print("\nLength of binary after conversion :- ",length)

    data = data + '*^*^*'

    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0
    for i in range(0,len(result),1): 
        res = bin(frame_bytes[j])[2:].zfill(8)
        if res[len(res)-4]== result[i]:
            frame_bytes[j] = (frame_bytes[j] & 253)      #253: 11111101
        else:
            frame_bytes[j] = (frame_bytes[j] & 253) | 2
            frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j = j + 1
    
    frame_modified = bytes(frame_bytes)

    stegofile=input("\nEnter name of the stego file (with extension) :- ")
    with wave.open(stegofile, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    print("\nEncoded the data successfully in the audio file.")    
    song.close()
def decode_aud_data():
    import wave

    nameoffile=input("Enter name of the file to be decoded :- ")
    song = wave.open(nameoffile, mode='rb')

    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    extracted = ""
    p=0
    for i in range(len(frame_bytes)):
        if(p==1):
            break
        res = bin(frame_bytes[i])[2:].zfill(8)
        if res[len(res)-2]==0:
            extracted+=res[len(res)-4]
        else:
            extracted+=res[len(res)-1]
    
        all_bytes = [ extracted[i: i+8] for i in range(0, len(extracted), 8) ]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "*^*^*":
                print("The Encoded data was :--",decoded_data[:-5])
                p=1
                break  
def aud_steg():
    while True:
        print("\n\t\tAUDIO STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            encode_aud_data()
        elif choice1 == 2:
            decode_aud_data()
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")
def KSA(key):
    key_length = len(key)
    S=list(range(256)) 
    j=0
    for i in range(256):
        j=(j+S[i]+key[i % key_length]) % 256
        S[i],S[j]=S[j],S[i]
    return S
def PRGA(S,n):
    i=0
    j=0
    key=[]
    while n>0:
        n=n-1
        i=(i+1)%256
        j=(j+S[i])%256
        S[i],S[j]=S[j],S[i]
        K=S[(S[i]+S[j])%256]
        key.append(K)
    return key
def preparing_key_array(s):
    return [ord(c) for c in s]
def encryption(plaintext):
    print("Enter the key : ")
    key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(plaintext)))
    plaintext=np.array([ord(i) for i in plaintext])

    cipher=keystream^plaintext
    ctext=''
    for c in cipher:
        ctext=ctext+chr(c)
    return ctext
def decryption(ciphertext):
    print("Enter the key : ")
    key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(ciphertext)))
    ciphertext=np.array([ord(i) for i in ciphertext])

    decoded=keystream^ciphertext
    dtext=''
    for c in decoded:
        dtext=dtext+chr(c)
    return dtext
def embed(frame):
    data=input("\nEnter the data to be Encoded in Video :") 
    data=encryption(data)
    print("The encrypted data is : ",data)
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')

    data +='*^*^*'
    
    binary_data=msgtobinary(data)
    length_data = len(binary_data)
    
    index_data = 0
    
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
        return frame
def extract(frame):
    data_binary = ""
    final_decoded_msg = ""
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*": 
                    for i in range(0,len(decoded_data)-5):
                        final_decoded_msg += decoded_data[i]
                    final_decoded_msg = decryption(final_decoded_msg)
                    print("\n\nThe Encoded data which was hidden in the Video was :--\n",final_decoded_msg)
                    return 
def encode_vid_data():
    cap=cv2.VideoCapture("covervideo_sample.mp4")
    vidcap = cv2.VideoCapture("covervideo_sample.mp4")    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))

    size = (frame_width, frame_height)
    out = cv2.VideoWriter('stegovideo.mp4',fourcc, 25.0, size)
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    cap.release()
    print("Total number of Frame in selected Video :",max_frame)
    print("Enter the frame number where you want to embed data : ")
    n=int(input())
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:    
            change_frame_with = embed(frame)
            frame_ = change_frame_with
            frame = change_frame_with
        out.write(frame)
    
    print("\nEncoded the data successfully in the video file.")
    return frame_
def decode_vid_data(frame_):
    cap = cv2.VideoCapture('stegovideo.mp4')
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    print("Total number of Frame in selected Video :",max_frame)
    print("Enter the secret frame number from where you want to extract data")
    n=int(input())
    vidcap = cv2.VideoCapture('stegovideo.mp4')
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:
            extract(frame_)
            return
def vid_steg():
    while True:
        print("\n\t\tVIDEO STEGANOGRAPHY OPERATIONS") 
        print("1. Encode the Text message")  
        print("2. Decode the Text message")  
        print("3. Exit")  
        choice1 = int(input("Enter the Choice:"))   
        if choice1 == 1:
            a=encode_vid_data()
        elif choice1 == 2:
            decode_vid_data(a)
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")
def main():
    print(r"""
   ▄████████     ███        ▄████████    ▄██████▄     ▄████████ ███▄▄▄▄            ███      ▄██████▄   ▄██████▄   ▄█          ▄█   ▄█▄  ▄█      ███     
  ███    ███ ▀█████████▄   ███    ███   ███    ███   ███    ███ ███▀▀▀██▄      ▀█████████▄ ███    ███ ███    ███ ███         ███ ▄███▀ ███  ▀█████████▄ 
  ███    █▀     ▀███▀▀██   ███    █▀    ███    █▀    ███    ███ ███   ███         ▀███▀▀██ ███    ███ ███    ███ ███         ███▐██▀   ███▌    ▀███▀▀██ 
  ███            ███   ▀  ▄███▄▄▄      ▄███          ███    ███ ███   ███          ███   ▀ ███    ███ ███    ███ ███        ▄█████▀    ███▌     ███   ▀ 
▀███████████     ███     ▀▀███▀▀▀     ▀▀███ ████▄  ▀███████████ ███   ███          ███     ███    ███ ███    ███ ███       ▀▀█████▄    ███▌     ███     
         ███     ███       ███    █▄    ███    ███   ███    ███ ███   ███          ███     ███    ███ ███    ███ ███         ███▐██▄   ███      ███     
   ▄█    ███     ███       ███    ███   ███    ███   ███    ███ ███   ███          ███     ███    ███ ███    ███ ███▌    ▄   ███ ▀███▄ ███      ███     
 ▄████████▀     ▄████▀     ██████████   ████████▀    ███    █▀   ▀█   █▀          ▄████▀    ▀██████▀   ▀██████▀  █████▄▄██   ███   ▀█▀ █▀      ▄████▀   
                                                                                                                 ▀           ▀                          
""")
    while True:  
        print("\n\t\t\tMAIN MENU\n")  
        print("1. IMAGE STEGANOGRAPHY {Hiding Text in Image cover file}")  
        print("2. TEXT STEGANOGRAPHY {Hiding Text in Text cover file}")  
        print("3. AUDIO STEGANOGRAPHY {Hiding Text in Audio cover file}")
        print("4. VIDEO STEGANOGRAPHY {Hiding Text in Video cover file}")
        print("5. Exit\n")  
        choice1 = int(input("Enter the Choice: "))   
        if choice1 == 1:
            img_steg()
        elif choice1 == 2:
            txt_steg()
        elif choice1 == 3:
            aud_steg()
        elif choice1 == 4:
            vid_steg()
        elif choice1 == 5:
            break
        else:
            print("Incorrect Choice")
        print("\n\n")
if __name__ == "__main__":
    main()
