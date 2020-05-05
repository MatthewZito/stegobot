import os
import shutil
import requests
import discord
from dotenv import load_dotenv
from steganography import Steganographer

class Cyrus(discord.Client):

    async def process_IO(self, message, data=None):
        tmp_fname = "tmp_out.png" if data == None else "tmp_in.png"
        try:
            img_url = message.attachments[0].url
            message.channel.send(f"[+] Downloading new image as tmp file...")
            print(f"[+] Downloading new image from {img_url}")
        except Exception as stderr:
            message.channel.send("[-] An error occurred; most likely malformed user-input.")
            print(f"[-] A command-level error occurred. See {stderr}")
        # open binary stream and write img as tmpfile
        try:
            img_stream = requests.get(img_url, stream=True)
            local_file = open(tmp_fname, 'wb')
            # set decode_content val to True, else dl size will be null
            img_stream.raw.decode_content = True
            # cp res stream raw data to local img file
            shutil.copyfileobj(img_stream.raw, local_file)
            # rm the img url res obj
            del img_stream
            await message.channel.send("[+] Image successfully downloaded as tmpf.")
            print("[+] Image successfully downloaded as tmp_file.")
        except Exception as stderr:
            await message.channel.send("[-] An error occurred during file download. An image must be attached to the command message.")
            print(f"[-] An error occurred during file download. See {stderr}")
        # initialize steganographer obj
        try:
            stego = Steganographer()
            await message.channel.send("[+] New Steganographer initialized.")
            print("[+] New Steganographer initialized.")
        except Exception as stderr:
            await message.channel.send("[-] An error occurred during Steganographer initialization.")
            print(f"[-] An error occurred during Steganographer initialization. See {stderr}")
        if (data != None):
            # encode
            try:
                filename = stego.encode(tmp_fname, data)
                print(filename)
                await message.channel.send("[+] Embedding data into image binary...")
                print("[+] Embedding data into image binary...")
            except Exception as stderr:
                await message.channel.send("[-] An error occurred during encoding. Try using a PNG.")
                print(f"[-] An error occurred during encoding. See {stderr}")
            # send new file
            try:
                await message.channel.send(file=discord.File(filename), content="[+] Provided data has been embedded in this image's binary:")
                print("[+] Successful upload.")
            except Exception as stderr:
                await message.channel.send("[-] An error occurred during file upload.")
                print(f"[-] An error occurred during file upload. See {stderr}")
        elif (data == None):
            # decode and send output
            try:
                data = stego.decode(tmp_fname)
                await message.channel.send(f"[+] Embedded data has been decoded: \n{data}")
                print("[+] Embedding data has been decoded.")
            except Exception as stderr:
                await message.channel.send("[-] An error occurred during decoding.")
                print(f"[-] An error occurred during decoding. See {stderr}")


    async def on_ready(self):
        print(f'{self.user} is now active.')

    async def on_message(self, message):
        if (message.author == client.user):
            return
        elif (not message.content.startswith("!stego")):
            return
        elif (message.content.startswith('!stego_encode')):
            if (message.attachments):
                data = " ".join(message.content.split()[1:])
                await self.process_IO(message, data)
        elif (message.content.startswith('!stego_decode')):
            if (message.attachments):
                await self.process_IO(message)
        else:
            return
      
load_dotenv()
TOKEN = os.getenv('CYRUS_TOKEN')
client = Cyrus()
client.run(TOKEN)