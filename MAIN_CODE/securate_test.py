from secrets import token_bytes
from configparser import RawConfigParser
def random_key(length):
    key = token_bytes(nbytes=length)
    key_int = int.from_bytes(key, 'big')
    return key_int

def encrypt(raw):
    raw_bytes = raw.encode()
    raw_int = int.from_bytes(raw_bytes, 'big')
    key_int = random_key(len(raw_bytes))
    return raw_int ^ key_int, key_int

def decrypt(encrypted, key_int):
    decrypted = encrypted ^ key_int
    length = (decrypted.bit_length() + 7) // 8
    decrypted_bytes = int.to_bytes(decrypted, length, 'big')
    return decrypted_bytes.decode()

if __name__ == "__main__":
    S = RawConfigParser()
    S.read("config.ini")
    d = S.get("time","starttime")
    print(d)
    S.set("time","starttime","2021-01-21T05:50:21")
    print(S.get("time","starttime"))
    try:
        with open("config.ini","w") as f:
            S.write(f)
            f.close()
    except Exception as d:
        print(str(d))
