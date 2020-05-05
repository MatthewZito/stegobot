from PIL import Image 

class Steganographer:
    def generate_binary(self, data): 
        """
        Convert given data into 8-bit binary using ASCII vals.
        Returns list of generated binary.
        """
        generated_data = []  
        for i in data: 
            generated_data.append(format(ord(i), "08b")) 
        return generated_data 
            
    def modify_pixels(self, pixels, data): 
        """
        Accepts as input the image pixels, and data obj. 
        Pixels are modified according to the 
        8-bit binary data returned as triumvirate tuples.
        """
        generated_data_list = self.generate_binary(data) 
        data_list_len = len(generated_data_list) 
        img_data = iter(pixels) 
    
        for i in range(data_list_len): 
            # extract three pixels each iteration
            pixel_triumvirate = [value for value in img_data.__next__()[:3] + img_data.__next__()[:3] + img_data.__next__()[:3]]            
            # set pixel val to odd for 1, even for 0 
            for j in range(0, 8): 
                if (generated_data_list[i][j]=="0") and (pixel_triumvirate[j]% 2 != 0): 
                    if (pixel_triumvirate[j]% 2 != 0): 
                        pixel_triumvirate[j] -= 1  
                elif (generated_data_list[i][j] == "1") and (pixel_triumvirate[j] % 2 == 0): 
                    pixel_triumvirate[j] -= 1
                    
            # Eighth pixel of every set determines when data is fully parsed.
            # 0 == keep reading; 1 == msg complete
            if (i == data_list_len - 1): 
                if (pixel_triumvirate[-1] % 2 == 0): 
                    pixel_triumvirate[-1] -= 1
            else: 
                if (pixel_triumvirate[-1] % 2 != 0): 
                    pixel_triumvirate[-1] -= 1
            pixel_triumvirate = tuple(pixel_triumvirate) 
            yield pixel_triumvirate[0:3] 
            yield pixel_triumvirate[3:6] 
            yield pixel_triumvirate[6:9] 
    
    def encode_enc(self, img, data): 
        w = img.size[0] 
        (x, y) = (0, 0) 
        for pixel in self.modify_pixels(img.getdata(), data): 
            # Putting modified pixels in the new image 
            img.putpixel((x, y), pixel) 
            if (x == w - 1): 
                x = 0
                y += 1
            else: 
                x += 1
                
    def encode(self, img_name, data): 
        """
        Steganographically encode given data into given image.
        Returns new image name.
        """
        image = Image.open(img_name, "r") 
        new_image = image.copy() 
        self.encode_enc(new_image, data) 
        file_name, file_ext = img_name.split(".")
        new_img_name = f"{file_name}_encoded.{file_ext}"
        new_image.save(new_img_name) 
        return new_img_name

    def decode(self, img_name):  
        """
        Decode data object steganographically embedded in given image.
        """
        image = Image.open(img_name, "r") 
        data = ""
        img_data = iter(image.getdata()) 
        while (True): 
            pixel_triumvirate = [value for value in img_data.__next__()[:3] +
                                    img_data.__next__()[:3] +
                                    img_data.__next__()[:3]] 
            # init a str as pointer for binary data 
            binary_str = "" 
            for i in pixel_triumvirate[:8]: 
                if (i % 2 == 0): 
                    binary_str += "0"
                else: 
                    binary_str += "1"
            data += chr(int(binary_str, 2)) 
            if (pixel_triumvirate[-1] % 2 != 0): 
                return data 

