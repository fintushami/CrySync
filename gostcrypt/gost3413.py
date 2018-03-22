from .utils import bytes2long
from .utils import long2bytes
from .utils import strxor
from .utils import xrange


def pad_size(data_size, blocksize):
    """Calculate required pad size to full up blocksize
    """
    if data_size < blocksize:
        return blocksize - data_size
    if data_size % blocksize == 0:
        return 0
    return blocksize - data_size % blocksize


def pad1(data, blocksize):
    """Padding method 1

    Just fill up with zeros if necessary.
    """
    return data + b"\x00" * pad_size(len(data), blocksize)


def pad2(data, blocksize):
    """Padding method 2 (also known as ISO/IEC 7816-4)

    Add one bit and then fill up with zeros.
    """
    return data + b"\x80" + b"\x00" * pad_size(len(data) + 1, blocksize)


def unpad2(data, blocksize):
    """Unpad method 2
    """
    last_block = bytearray(data[-blocksize:])
    pad_index = last_block.rfind(b"\x80")
    if pad_index == -1:
        raise ValueError("Invalid padding")
    for c in last_block[pad_index + 1:]:
        if c != 0:
            raise ValueError("Invalid padding")
    return data[:-(blocksize - pad_index)]


def pad3(data, blocksize):
    """Padding method 3
    """
    if pad_size(len(data), blocksize) == 0:
        return data
    return pad2(data, blocksize)


def ecb_encrypt(encrypter, bs, pt):
    """ECB encryption mode of operation

    :param encrypter: Encrypting function, that takes block as an input
    :param int bs: cipher's blocksize
    :param bytes pt: already padded plaintext
    """
    if not pt or len(pt) % bs != 0:
        raise ValueError("Plaintext is not blocksize aligned")
    ct = []
    for i in xrange(0, len(pt), bs):
        ct.append(encrypter(pt[i:i + bs]))
    return b"".join(ct)


def ecb_decrypt(decrypter, bs, ct):
    """ECB decryption mode of operation

    :param decrypter: Decrypting function, that takes block as an input
    :param int bs: cipher's blocksize
    :param bytes ct: ciphertext
    """
    if not ct or len(ct) % bs != 0:
        raise ValueError("Ciphertext is not blocksize aligned")
    pt = []
    for i in xrange(0, len(ct), bs):
        pt.append(decrypter(ct[i:i + bs]))
    return b"".join(pt)


def ctr(encrypter, bs, data, iv):
    """Counter mode of operation

    :param encrypter: Encrypting function, that takes block as an input
    :param int bs: cipher's blocksize
    :param bytes data: plaintext/ciphertext
    :param bytes iv: half blocksize-sized initialization vector

    For decryption you use the same function again.
    """
    if len(iv) != bs // 2:
        raise ValueError("Invalid IV size")
    stream = []
    ctr_value = 0
    for _ in xrange(0, len(data) + pad_size(len(data), bs), bs):
        stream.append(encrypter(iv + long2bytes(ctr_value, bs // 2)))
        ctr_value += 1
    return strxor(b"".join(stream), data)


def ofb(encrypter, bs, data, iv):
    """OFB mode of operation

    :param encrypter: Encrypting function, that takes block as an input
    :param int bs: cipher's blocksize
    :param bytes data: plaintext/ciphertext
    :param bytes iv: double blocksize-sized initialization vector

    For decryption you use the same function again.
    """
    if len(iv) < 2 * bs or len(iv) % bs != 0:
        raise ValueError("Invalid IV size")
    r = [iv[i:i + bs] for i in range(0, len(iv), bs)]
    result = []
    for i in xrange(0, len(data) + pad_size(len(data), bs), bs):
        r = r[1:] + [encrypter(r[0])]
        result.append(strxor(r[-1], data[i:i + bs]))
    return b"".join(result)


def cbc_encrypt(encrypter, bs, pt, iv):
    """CBC encryption mode of operation

    :param encrypter: Encrypting function, that takes block as an input
    :param int bs: cipher's blocksize
    :param bytes pt: already padded plaintext
    :param bytes iv: double blocksize-sized initialization vector
    """
    if not pt or len(pt) % bs != 0:
        raise ValueError("Plaintext is not blocksize aligned")
    if len(iv) < 2 * bs or len(iv) % bs != 0:
        raise ValueError("Invalid IV size")
    r = [iv[i:i + bs] for i in range(0, len(iv), bs)]
    ct = []
    for i in xrange(0, len(pt), bs):
        ct.append(encrypter(strxor(r[0], pt[i:i + bs])))
        r = r[1:] + [ct[-1]]
    return b"".join(ct)


def cbc_decrypt(decrypter, bs, ct, iv):
    """CBC decryption mode of operation

    :param decrypter: Decrypting function, that takes block as an input
    :param int bs: cipher's blocksize
    :param bytes ct: ciphertext
    :param bytes iv: double blocksize-sized initialization vector
    """
    if not ct or len(ct) % bs != 0:
        raise ValueError("Ciphertext is not blocksize aligned")
    if len(iv) < 2 * bs or len(iv) % bs != 0:
        raise ValueError("Invalid IV size")
    r = [iv[i:i + bs] for i in range(0, len(iv), bs)]
    pt = []
    for i in xrange(0, len(ct), bs):
        blk = ct[i:i + bs]
        pt.append(strxor(r[0], decrypter(blk)))
        r = r[1:] + [blk]
    return b"".join(pt)


def cfb_encrypt(encrypter, bs, pt, iv):
    """CFB encryption mode of operation

    :param encrypter: Encrypting function, that takes block as an input
    :param int bs: cipher's blocksize
    :param bytes pt: plaintext
    :param bytes iv: double blocksize-sized initialization vector
    """
    if len(iv) < 2 * bs or len(iv) % bs != 0:
        raise ValueError("Invalid IV size")
    r = [iv[i:i + bs] for i in range(0, len(iv), bs)]
    ct = []
    for i in xrange(0, len(pt) + pad_size(len(pt), bs), bs):
        ct.append(strxor(encrypter(r[0]), pt[i:i + bs]))
        r = r[1:] + [ct[-1]]
    return b"".join(ct)


def cfb_decrypt(encrypter, bs, ct, iv):
    """CFB decryption mode of operation

    :param encrypter: Encrypting function, that takes block as an input
    :param int bs: cipher's blocksize
    :param bytes ct: ciphertext
    :param bytes iv: double blocksize-sized initialization vector
    """
    if len(iv) < 2 * bs or len(iv) % bs != 0:
        raise ValueError("Invalid IV size")
    r = [iv[i:i + bs] for i in range(0, len(iv), bs)]
    pt = []
    for i in xrange(0, len(ct) + pad_size(len(ct), bs), bs):
        blk = ct[i:i + bs]
        pt.append(strxor(encrypter(r[0]), blk))
        r = r[1:] + [blk]
    return b"".join(pt)


def _mac_shift(bs, data, xor_lsb=0):
    num = (bytes2long(data) << 1) ^ xor_lsb
    return long2bytes(num, bs)[-bs:]


def _mac_ks(encrypter, bs):
    Rb = 0b10000111 if bs == 16 else 0b11011
    _l = encrypter(bs * b'\x00')
    k1 = _mac_shift(bs, _l, Rb) if bytearray(_l)[0] & 0x80 > 0 else _mac_shift(bs, _l)
    k2 = _mac_shift(bs, k1, Rb) if bytearray(k1)[0] & 0x80 > 0 else _mac_shift(bs, k1)
    return k1, k2


def mac(encrypter, bs, data):
    """MAC (known here as CMAC, OMAC1) mode of operation

    :param encrypter: Encrypting function, that takes block as an input
    :param int bs: cipher's blocksize
    :param bytes data: data to authenticate

    Implementation is based on PyCrypto's CMAC one, that is in public domain.
    """
    k1, k2 = _mac_ks(encrypter, bs)
    if len(data) % bs == 0:
        tail_offset = len(data) - bs
    else:
        tail_offset = len(data) - (len(data) % bs)
    prev = bs * b'\x00'
    for i in xrange(0, tail_offset, bs):
        prev = encrypter(strxor(data[i:i + bs], prev))
    tail = data[tail_offset:]
    return encrypter(strxor(
        strxor(pad3(tail, bs), prev),
        k1 if len(tail) == bs else k2,
    ))
