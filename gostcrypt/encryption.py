from gostcrypt.gost3413 import pad2, unpad2
from gostcrypt.utils import strxor
from gostcrypt.gost3412 import GOST3412Kuznechik

BLOCK_SIZE = 16  # Bytes
pad_size = lambda s: BLOCK_SIZE - len(s) % BLOCK_SIZE


class BasicEncryptor:
    def __init__(self, key):
        assert isinstance(key, bytes)
        self.key = key
        self.cryptor = GOST3412Kuznechik(self.key)

    def _encrypt(self, msg):
        return self.cryptor.encrypt(msg)

    def _decrypt(self, msg):
        return self.cryptor.decrypt(msg)

#
# class CommandEncryptor(BasicEncryptor):
#     def __init__(self, key, mode='cbc'):
#         super(CommandEncryptor,self).__init__(key)
#         if mode=='cbc':
#             self.encryption_method = cbc_encrypt
#             self.decryption_method = cbc_decrypt
#
#         elif mode=='cfb':
#             self.encryption_method = cfb_encrypt
#             self.decryption_method = cfb_decrypt
#
#     def encrypt_command(self, message, iv):
#         if len(message) % 16 != 0:
#             message = pad2(message,len(message)+pad_size(message))
#         return self.encryption_method(self.cryptor.encrypt,BLOCK_SIZE,message,iv)
#
#     def decrypt_command(self, message, iv):
#         return unpad2(self.decryption_method(self.cryptor.decrypt,BLOCK_SIZE,message,iv), BLOCK_SIZE)

class cbcEncryptor(BasicEncryptor):

    def __init__(self, key):
        super(cbcEncryptor, self).__init__(key)

    def init(self, iv):
        self.r = [iv[i:i + BLOCK_SIZE] for i in range(0, len(iv), BLOCK_SIZE)]
        self.ct = []

    def update_encrypt(self, block):
        # chunk = self.cryptor.encrypt(strxor(self.r[0], block))
        chunk = self._encrypt(strxor(self.r[0], block))
        self.ct.append(chunk)
        self.r = self.r[1:] + [self.ct[-1]]
        return chunk

    def update_decrypt(self, block):
        # chunk = strxor(self.r[0], self.cryptor.decrypt(block))
        chunk = strxor(self.r[0], self._decrypt(block))
        self.ct.append(chunk)
        self.r = self.r[1:] + [block]
        return chunk


class MsgEncryptor:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt_msg(self, pt):
        if len(pt) % 16 != 0:
            pt = pad2(pt, len(pt)+pad_size(pt))
        E = cbcEncryptor(self.key)
        E.init(self.iv)
        C = []
        for i in range(0, len(pt), BLOCK_SIZE):
            S = E.update_encrypt(pt[i:i + BLOCK_SIZE])
            C.append(S)
        return b"".join(C)

    def decrypt_msg(self, ct):
        E = cbcEncryptor(self.key)
        E.init(self.iv)
        C = []
        for i in range(0, len(ct), BLOCK_SIZE):
            S = E.update_decrypt(ct[i:i + BLOCK_SIZE])
            C.append(S)
        return unpad2(b"".join(C), BLOCK_SIZE)
