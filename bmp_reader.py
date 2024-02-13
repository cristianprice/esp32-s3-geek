class BMPReader(object):
    def __init__(self, filename):
        self._filename = filename
        self._read_img_info()
    def get_buf(self,data_len:int,start:int=0):
        assert data_len%2 == 0,\
            "return data RGB565,the length have to be a multiple of 2"
        assert start%2 == 0,\
            "return data RGB565,the startpos have to be a multiple of 2"
        buffer=bytearray(data_len)
        with open(self._filename, 'rb') as f:
            f.seek(self.start_pos+(int(start/2*3)))
            img_bytes = bytearray(f.read(int(data_len/2*3)))
            f.close()
        for x in range (int(data_len/2)):

            r=img_bytes[x*3+2]
            g=img_bytes[x*3+1]
            b=img_bytes[x*3]

            img_data = ((r&0xf8)<<8) | ((g&0xf8)<<3) | ((b&0xf8)>>3)
            buffer[x*2]  =   img_data&0xff  
            buffer[x*2+1]= (img_data>>8)&0xff
        img_bytes=0
        return buffer

    def _read_img_info(self):
        def lebytes_to_int(bytes):
            n = 0x00
            while len(bytes) > 0:
                n <<= 8
                n |= bytes.pop()
            return int(n)

        with open(self._filename, 'rb') as f:
            img_bytes = list((f.read(38)))
            f.close()
        # Before we proceed, we need to ensure certain conditions are met
        assert img_bytes[0:2] == [66, 77], "Not a valid BMP file"
        assert lebytes_to_int(img_bytes[30:34]) == 0, \
            "Compression is not supported"
        assert lebytes_to_int(img_bytes[28:30]) == 24, \
            "Only 24-bit colour depth is supported"

        self.start_pos = lebytes_to_int(img_bytes[10:14])
        self.end_pos = self.start_pos + lebytes_to_int(img_bytes[34:38])

        self.width = lebytes_to_int(img_bytes[18:22])
        self.height = lebytes_to_int(img_bytes[22:26])