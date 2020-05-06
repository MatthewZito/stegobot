# Stegobot: A Steganographic Image Rendering Bot
Stegobot is a Python-powered Discord bot which enables users to steganographically embed data inside of images. 
![Demo](https://github.com/MatthewZito/stegobot/blob/master/assets/stegobot_demo.gif)

## Documentation
Stegobot accepts two commands, both issued as prefixed messages accompanied by an image attachment. An attached image will have the following format for encoding:
```
!stego_encode This will be the steganographically encoded message
```
An attached image (with a steganographically embedded data object) as applied with the decode command is quite simply:
```
!stego_decode
```
Stegobot automates the same process for both encoding and decoding data objects; the divergence occurs after instantiating the Steganographer and calling either its encode or decode class methods.

The Steganographer module accepts as input an image and, if encoding, a string of data to be embedded in said image. This means our bot needs to be able to pull the image attachment (and data, if applicable) in order to feed it to the Steganographer. Stegobot downloads all given attachments as tempfiles via a binary stream:

```
 async def process_IO(self, message, data=None):
        tmp_fname = "tmp_out.png" if data == None else "tmp_in.png"
        img_url = message.attachments[0].url
        ...
        ...
        ...
        img_stream = requests.get(img_url, stream=True)
        local_file = open(tmp_fname, 'wb')
        # set decode_content val to True, else dl size will be null
        img_stream.raw.decode_content = True
        # cp res stream raw data to local img file
        shutil.copyfileobj(img_stream.raw, local_file)
        # rm the img url res obj
        del img_stream
        await message.channel.send("[+] Image successfully downloaded as tmpf.")
```

If the Steganographer's encoding method has been called, we first begin with the user-input data:
```
def generate_binary(self, data): 
        """
        Convert given data into 8-bit binary using ASCII vals.
        Returns list of generated binary.
        """
        generated_data = []  
        for i in data: 
            generated_data.append(format(ord(i), "08b")) 
        return generated_data 
```

Each byte of the given data is mapped to its corresponding 8-bit binary value qua ASCII. Next, the given image is deconstructed into its byte-code representation. This byte-code object is then parsed in sets of three bytes; the LSB of a selected pixel is then modified to even/odd so as to signify the binary value sequence of the mapped data.

The Steganographer reassembles the image, now with the steganographically embedded data object, and returns it to Stegobot, which in turn uploads the image to Discord. Now, the only place this data object will ever be decoded is here. In short, one can generate an image carrying sensitive information and deliver this information without the context of Discord. For secure decoding, the recipient must then later decode within the context of Discord. 

I suppose this paradigm plays upon taking advatange of the nuances of blatantly insecure channels for otherwise clandestine communications. It should be noted here that Stegobot's embeds are certainly not impervious to decryption, though doing so is certainly difficult (if you even know to be looking for a data object in the image to begin with).

To decode an encrypted message, Stegobot reiterates the aforementioned process but instead calls the Steganographer's decode method with the tempfile as its argument and returns - to Discord - the decoded data.

Note: This project was made for personal enjoyment; as such, I am not accepting contributions nor actively maintaining this project.
