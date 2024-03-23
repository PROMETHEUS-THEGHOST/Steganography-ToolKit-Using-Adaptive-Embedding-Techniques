# Steganography-ToolKit-Using-Adaptive-Embedding-Techniques: 
**Made by - Vaisakh Sriram**
This project mainly showcases the adaptive algorithms to hide text message in four different cover file **Text, Image, Audio, Video** and transfer it to the receiver who can extract the hidden message from these files with the same tools.

**Text Steganography :**
We hide text in a text file using, ZWCs.
ZWCs-ZWCs- In Unicode, there are specific zero-width characters (ZWC) that are used to control special entities such as Zero Width Non Joiner (e.g., ZWNJ separates two letters in special languages) and POP directional, which have no written symbol or width in digital text.
* We get its ascii value and it is incremented or decremented based on if ascii value between 32 and 64 , it is incremented by 48(ascii value for 0) else it is decremented by 48.
* Then xor the the obtained value with 170(binary equivalent-10101010) .
* Convert the obtained number from first two step to its binary equivalent then add "0011" if it earlier belonged to ascii value between 32 and 64 else add "0110" making it 12 bit for each character.
* With the final binary equivalent we also 111111111111 as delimiter to find the end of message.
* Now from 12 bit representing each character every 2 bit is replaced with equivalent ZWCs according to the table. Each character is hidden after a word in the cover text.
