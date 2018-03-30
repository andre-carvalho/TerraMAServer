import os, errno, base64
# import binascii
from PIL import Image
from io import BytesIO


class B64Utils():

   #constructor
    def __init__(self, path, base64_string=None):
        self.b64 = base64_string
        self.path = path

    def base64Decode(self):
        """Add missing padding to string and return the decoded base64 string."""
        self.b64 = str(self.b64).strip()
        try:
            return base64.b64decode(self.b64)
        except TypeError:
            padding = len(self.b64) % 4
            if padding == 1:
                return ''
            elif padding == 2:
                self.b64 += b'=='
            elif padding == 3:
                self.b64 += b'='
            return base64.b64decode(self.b64)

    def writeToBinary(self, sufix):
        b64out = self.base64Decode()
        im = Image.open(BytesIO(b64out))
        file_ext = im.format.lower()
        path = '{0}/image{1}.{2}'.format(self.path, sufix, file_ext)
        output_file = open(path,'wb')
        output_file.write(b64out)
        output_file.close()

    def readFromBinary(self, sufix):
        file_ext = 'png'
        mimetype = 'image/{0}'.format(file_ext)
        file_name = 'image{0}.{1}'.format(sufix, file_ext)
        path = '{0}/{1}'.format(self.path, file_name)
        if os.path.exists(path):
            output_file = open(path,'rb')
            binary = output_file.read()
            output_file.close()
        else:
            raise FileNotFoundError(errno.ENOENT, 'Image file not found')
        
        return BytesIO(binary), file_name, mimetype