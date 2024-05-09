# Steganography-ToolKit-Using-Adaptive-Embedding-Techniques: 
**Made by - Vaisakh Sriram**

This project mainly showcases the adaptive algorithms to hide text message in four different cover file **Text, Image, Audio, Video** and transfer it to the receiver who can extract the hidden message from these files with the same tools.


![image](https://github.com/VAISAKH-SRIRAM/Steganography-ToolKit-Using-Adaptive-Embedding-Techniques/assets/119421107/fd904a07-3365-4953-8597-fc1ec1da408a)


# **Text Steganography :**
We hide text in a text file using, ZWCs.
ZWCs-ZWCs- In Unicode, there are specific zero-width characters (ZWC) that are used to control special entities such as Zero Width Non Joiner (e.g., ZWNJ separates two letters in special languages) and POP directional, which have no written symbol or width in digital text.
* We get its ascii value and it is incremented or decremented based on if ascii value between 32 and 64 , it is incremented by 48(ascii value for 0) else it is decremented by 48.
* Then xor the the obtained value with 170(binary equivalent-10101010) .
* Convert the obtained number from first two step to its binary equivalent then add "0011" if it earlier belonged to ascii value between 32 and 64 else add "0110" making it 12 bit for each character.
* With the final binary equivalent we also 111111111111 as delimiter to find the end of message.
* Now from 12 bit representing each character every 2 bit is replaced with equivalent ZWCs according to the table. Each character is hidden after a word in the cover text.
  
# **Image Steganography :**
In this we hide text message in an image file, using Modified LSB Algorithm where we overwrite the LSB bit of actual image with the bit of text message character. At the end of text message we push a delimiter to the message string as a checkpoint useful in decoding function. We encode data in order of Red, then Green and then Blue pixel for the entire message.

# **Audio Steganography :**
We will be using Cover Audio as a Cover file to encode the given text. Wave module is used to read the audio file. Firstly we convert our secret message to its binary equivalent and added delimiter '*****' to the end of the message. For encoding we have modified the LSB Algorithm, for that we take each frame byte of the converting it to 8 bit format then check for the 4th LSB and see if it matches with the secret message bit. If yes, change the 2nd LSB to 0 using the logical AND operator between each frame byte and 253(11111101). Else we change the 2nd LSB to 1  using logical AND operation with 253 and then logical OR to change it to 1 and now add secret message bit in LSB for achieving that use logical AND operation between each frame byte of carrier audio and a binary number of 254 (11111110). Then logical OR operation between modified carrier byte and the next bit (0 or 1) from the secret message which resets the LSB of the carrier byte.

# **Video Steganography :**
In video steganography we have used combination of cryptography and Steganography. We encode the message through two parts:-
* We convert plaintext to cipher text for doing so we have used RC4 Encryption Algorithm. RC4 is a stream cipher and variable-length key algorithm. This algorithm encrypts one byte at a time. It has two major parts for encryption and decryption:-
* KSA(Key-Scheduling Algorithm)- A list S of length 256 is made and the entries of S are set equal to the values from 0 to 255 in ascending order. We ask user for a key and convert it to its equivalent ascii code. S[] is a permutation of 0,1,2....255, now a variable j is assigned as j=(j+S[i]+key[i%key_length) mod 256 and swap S(i) with S(j) and accordingly we get new permutation for the whole keystream according to the key.
* PRGA(Pseudo random generation Algorithm (Stream Generation)) - Now we take input length of plaintext and initiate loop to generate a keystream byte of equal length. For this we initiate i=0, j=0 now increment i by 1 and mod with 256. Now we add S[i] to j amd mod of it with 256 ,again swap the values. At last step take store keystreambytes which matches as S[(S[i]+S[j]) mod 256] to finally get key stream of length same as plaintext.
* Now we xor the plaintext with keystream to get the final cipher.

### Procedure

**OPEN TERMINAL AND PASTE THIS COMMAND ON IT AND CLONE MY REPOSITORY**

**NOTE :**  *GIT is required in your system to clone this repo if your system doesn't have it please install it from here :  [Git Downloads for Windows](https://git-scm.com/download/win)*
  ```bash
  git clone https://github.com/VAISAKH-SRIRAM/Steganography-ToolKit-Using-Adaptive-Embedding-Techniques.git
  ```
 **THEN INSTALL THE CODE REQUIREMENTS BY RUNNING THIS COMMAND IN THE TERMINAL**
  ```bash
  pip install -r requirements.txt
  ```
  **THEN RUN OUR MAIN CODE IN THE TERMINAL** *[ OR IN VS CODE ]*
  ```bash
  python corrcode.py
  ```
  
