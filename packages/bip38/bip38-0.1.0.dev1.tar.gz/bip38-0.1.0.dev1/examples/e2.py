#!/usr/bin/env python3

from typing import (
    Tuple, Union, Optional
)
from pyaes import AESModeOfOperationECB

import scrypt
import unicodedata
import os

from bip38.utils import (
    integer_to_bytes, bytes_to_integer, get_bytes, sha256, ripemd160
)
from bip38.libs.base58 import (
    encode, decode, ensure_string
)

# Bitcoin address prefix
ADDRESS_PREFIX: int = 0X00
# Wallet important format prefix
WIF_PREFIX: int = 0x80
# BIP38 non-EC-multiplied private key prefix
BIP38_NON_EC_PRIVATE_KEY_PREFIX: int = 0x0142
# BIP38 EC-multiplied private key prefix
BIP38_EC_PRIVATE_KEY_PREFIX: int = 0x0143
# Private key prefixes
UNCOMPRESSED_PRIVATE_KEY_PREFIX: int = 0x00
COMPRESSED_PRIVATE_KEY_PREFIX: int = 0x01
# The proven prime
P_CURVE: int = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
# Number of points in the field
N: int = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
# These two defines the elliptic curve. y^2 = x^3 + A-curve * x + B-curve
A_CURVE: int = 0
B_CURVE: int = 7
# This is our generator point. Trillions of dif ones possible
G_POINT: Tuple[int, int] = (
    55066263022277343669578718895168534326250603453777594175500187360389116729240,
    32670510020758816978083085130507043184471273380659243275938904335757337482424
)
# Public key prefixes
EVEN_COMPRESSED_PUBLIC_KEY_PREFIX: int = 0x02
ODD_COMPRESSED_PUBLIC_KEY_PREFIX: int = 0x03
UNCOMPRESSED_PUBLIC_KEY_PREFIX: int = 0x04
# Checksum byte length
CHECKSUM_BYTE_LENGTH: int = 4


# Greatest common divisor: Extended Euclidean Algorithm/'division' in elliptic curves
def mod_inv(a: int, n: int = P_CURVE) -> int:
    lm, hm = 1, 0
    resto = a % n
    high = n
    while resto > 1:
        ratio = high // resto
        nm = hm - lm * ratio
        new = high - resto * ratio
        lm, resto, hm, high = nm, new, lm, resto
    return lm % n


# Not true addition, invented for EC. Could have been called anything
def ec_add(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    LamAdd = ((b[1] - a[1]) * mod_inv(b[0] - a[0], P_CURVE)) % P_CURVE
    x = (LamAdd * LamAdd - a[0] - b[0]) % P_CURVE
    y = (LamAdd * (a[0] - x) - a[1]) % P_CURVE
    return x, y


# This is called point doubling, also invented for EC
def ec_double(a: Tuple[int, int]) -> Tuple[int, int]:
    Lam = ((3 * a[0] * a[0] + A_CURVE) * mod_inv((2 * a[1]), P_CURVE)) % P_CURVE
    x = (Lam * Lam - 2 * a[0]) % P_CURVE
    y = (Lam * (a[0] - x) - a[1]) % P_CURVE
    return x, y


# Double & add. Not true multiplication
def ecc_multiply(gen_point: tuple, scalar_hex: int) -> Tuple[int, int]:
    if scalar_hex == 0 or scalar_hex >= N:
        raise ValueError("Invalid scalar or private key")
    # Binary string without beginning 0b
    scalar_bin = str(bin(scalar_hex))[2:]
    # This is a tuple of two integers of the point of generation of the curve
    q: Tuple[int, int] = gen_point
    for i in range(1, len(scalar_bin)):
        q = ec_double(q)
        if scalar_bin[i] == "1":
            q = ec_add(q, gen_point)
    return q


def private_key_to_public_key(private_key: Union[str, bytes], public_key_type: str = "compressed") -> str:
    # Get the public key point
    x, y = ecc_multiply(
        G_POINT, bytes_to_integer(get_bytes(private_key))
    )

    if public_key_type == "uncompressed":
        public_uncompressed: bytes = (
            integer_to_bytes(UNCOMPRESSED_PUBLIC_KEY_PREFIX) + integer_to_bytes(x) + integer_to_bytes(y)
        )
        return public_uncompressed.hex()
    elif public_key_type == "compressed":
        public_compressed: bytes = (
            (   # If the Y value for the Public Key is odd
                integer_to_bytes(ODD_COMPRESSED_PUBLIC_KEY_PREFIX) + integer_to_bytes(x)
            ) if y & 1 else (
                integer_to_bytes(EVEN_COMPRESSED_PUBLIC_KEY_PREFIX) + integer_to_bytes(x)
            )   # Or else, if the Y value is even
        )
        return public_compressed.hex()
    else:
        raise ValueError("Invalid WIF type, choose only 'uncompressed' or 'compressed' types")


def get_checksum(raw: bytes) -> bytes:
    return sha256(sha256(raw))[:CHECKSUM_BYTE_LENGTH]


def encode_wif(private_key: Union[str, bytes]) -> Tuple[str, str]:

    if len(get_bytes(private_key)) != 32:
        raise ValueError(f"Invalid private key length (expected 64, got {len(private_key)!r})")

    wif_payload: bytes = (
        integer_to_bytes(WIF_PREFIX) + get_bytes(private_key)
    )
    wif_compressed_payload: bytes = (
        integer_to_bytes(WIF_PREFIX) + get_bytes(private_key) + integer_to_bytes(COMPRESSED_PRIVATE_KEY_PREFIX)
    )

    return (
        encode(wif_payload + get_checksum(wif_payload)),
        encode(wif_compressed_payload + get_checksum(wif_compressed_payload))
    )


def private_key_to_wif(private_key: Union[str, bytes], wif_type: str = "wif-compressed") -> str:
    # Getting uncompressed and compressed
    wif, wif_compressed = encode_wif(private_key=private_key)

    if wif_type == "wif":
        return wif
    elif wif_type == "wif-compressed":
        return wif_compressed
    else:
        raise ValueError("Invalid WIF type, choose only 'uncompressed' or 'compressed' types")


def decode_wif(wif: str) -> Tuple[str, str, str]:

    raw: bytes = decode(wif)
    if not raw.startswith(integer_to_bytes(0x80)):
        raise ValueError(f"Invalid wallet important format")

    prefix_length: int = len(integer_to_bytes(WIF_PREFIX))
    prefix_got: bytes = raw[:prefix_length]
    if integer_to_bytes(WIF_PREFIX) != prefix_got:
        raise ValueError(f"Invalid WIF prefix (expected {prefix_length!r}, got {prefix_got!r})")

    raw_without_prefix: bytes = raw[prefix_length:]

    checksum: bytes = raw_without_prefix[-1 * 4:]
    private_key: bytes = raw_without_prefix[:-1 * 4]
    wif_type: str = "wif"

    if len(private_key) not in [33, 32]:
        raise ValueError(f"Invalid wallet important format")
    elif len(private_key) == 33:
        private_key = private_key[:-len(integer_to_bytes(COMPRESSED_PRIVATE_KEY_PREFIX))]
        wif_type = "wif-compressed"

    return private_key.hex(), wif_type, checksum.hex()


def wif_to_private_key(wif: str) -> str:
    return decode_wif(wif=wif)[0]


def get_wif_type(wif: str) -> str:
    return decode_wif(wif=wif)[1]


def get_wif_checksum(wif: str) -> str:
    return decode_wif(wif=wif)[2]


def public_key_to_addresses(public_key: Union[str, bytes]) -> str:
    # Getting public key hash
    public_key_hash: bytes = ripemd160(sha256(get_bytes(public_key)))
    payload: bytes = (
        integer_to_bytes(ADDRESS_PREFIX) + public_key_hash
    )
    return ensure_string(encode(payload + get_checksum(payload)))


def bip38_encrypt(wif: str, passphrase: str) -> str:

    wif_type: str = get_wif_type(wif=wif)
    public_key_type: Optional[str] = None
    private_key: Optional[str] = None
    flag: Optional[bytes] = None

    if wif_type == "wif":
        flag = b'\xc0'
        private_key = wif_to_private_key(wif=wif)
        public_key_type = "uncompressed"
    elif wif_type == "wif-compressed":
        flag = b'\xe0'
        private_key = wif_to_private_key(wif=wif)
        public_key_type = "compressed"

    public_key: str = private_key_to_public_key(
        private_key=private_key, public_key_type=public_key_type
    )
    address: str = public_key_to_addresses(public_key=public_key)
    address_hash: bytes = get_checksum(address.encode())
    key: bytes = scrypt.hash(unicodedata.normalize('NFC', passphrase), address_hash, 16384, 8, 8)
    derived_half_1, derived_half_2 = key[0:32], key[32:64]

    aes: AESModeOfOperationECB = AESModeOfOperationECB(derived_half_2)
    encrypted_half_1 = aes.encrypt(get_bytes(
        '%0.32x' % (int(private_key[0:32], 16) ^ int(derived_half_1[0:16].hex(), 16))
    ))
    encrypted_half_2 = aes.encrypt(get_bytes(
        '%0.32x' % (int(private_key[32:64], 16) ^ int(derived_half_1[16:32].hex(), 16))
    ))

    encrypted_privkey: bytes = (
        integer_to_bytes(BIP38_EC_PRIVATE_KEY_PREFIX) + flag + address_hash + encrypted_half_1 + encrypted_half_2
    )
    return ensure_string(encode(
        encrypted_privkey + get_checksum(encrypted_privkey)
    ))

#
# def bip38_decrypt(encrypted_wif: str, passphrase: str) -> str:
#
#     encrypted_wif_decode: bytes = decode(encrypted_wif)
#     if len(encrypted_wif_decode) != 78:
#         raise ValueError(f"Invalid encrypted WIF (expected 78, got {len(encrypted_wif_decode)!r})")
#
#     prefix: bytes = encrypted_wif_decode[:2]
#
#     if prefix == integer_to_bytes(BIP38_NON_EC_PRIVATE_KEY_PREFIX):
#         print(prefix.hex())
#     elif prefix == integer_to_bytes(BIP38_EC_PRIVATE_KEY_PREFIX):
#         pass
#     else:
#         raise ValueError(f"Invalid encrypted wallet important format")
#
#
#     d = d[2:]
#     flag: bytes = d[0:1]
#
#     d = d[1:]
#     if flagbyte == '\xc0':
#         compressed = False
#     if flagbyte == '\xe0':
#         compressed = True
#     addresshash = d[0:4]
#     d = d[4:-4]
#     key = scrypt.hash(passphrase, addresshash, 16384, 8, 8)
#     derivedhalf1 = key[0:32]
#     derivedhalf2 = key[32:64]
#     encryptedhalf1 = d[0:16]
#     encryptedhalf2 = d[16:32]
#     aes = AES.new(derivedhalf2)
#     decryptedhalf2 = aes.decrypt(encryptedhalf2)
#     decryptedhalf1 = aes.decrypt(encryptedhalf1)
#     priv = decryptedhalf1 + decryptedhalf2
#     priv = binascii.unhexlify('%064x' % (long(binascii.hexlify(priv), 16) ^ long(binascii.hexlify(derivedhalf1), 16)))
#     pub = privtopub(priv)
#     if compressed:
#         pub = encode_pubkey(pub, 'hex_compressed')
#         wif = encode_privkey(priv, 'wif_compressed')
#     else:
#         wif = encode_privkey(priv, 'wif')
#     addr = pubtoaddr(pub)
#     if hashlib.sha256(hashlib.sha256(addr).digest()).digest()[0:4] != addresshash:
#         print('Addresshash verification failed! Password is likely incorrect.')
#
#     return wif
#
#
# def intermediate_code(password, useLotAndSequence=False, lot=100000, sequence=1, owner_salt=os.urandom(8)):
#
#     # password = normalize_input(password, False, True)
#
#     assert len(owner_salt) == 8 or (len(owner_salt) == 4 and useLotAndSequence)
#
#     from binascii import hexlify
#
#     if useLotAndSequence:
#         lot, sequence = int(lot), int(sequence)
#         assert 100000 <= lot <= 999999
#         assert 0 <= sequence <= 4095
#         lotsequence = integer_to_bytes((lot*4096 + sequence), 4)
#         owner_salt = owner_salt[:4]
#         prefactor = scrypt.hash(password, owner_salt, 16384, 8, 8, 32)
#         prefactor = hexlify(prefactor)
#         owner_entropy = hexlify(owner_salt) + lotsequence
#         passfactor = sha256(prefactor + owner_entropy)
#         magicbytes = '2ce9b3e1ff39e251'
#     else:
#         passfactor = scrypt.hash(password, owner_salt, 16384, 8, 8, 32)
#         passfactor = hexlify(passfactor)
#         owner_entropy = hexlify(owner_salt)
#         magicbytes = '2ce9b3e1ff39e253'
#     # print(passfactor, len("f1a84c46a8ee748fc839a94bca0b9ab75c18de167c7cdbeb4d0999e75fef2bfa"))
#     passpoint = private_key_to_public_key(passfactor.hex(), "compressed")
#     return ensure_string(encode(get_bytes(magicbytes + owner_entropy.hex() + passpoint)))
#
# import hashlib
# from binascii import unhexlify, hexlify
# from Crypto.Cipher import AES
# from simplebitcoinfuncs import *
# from simplebitcoinfuncs.hexhashes import *
# from simplebitcoinfuncs.ecmath import N
#
# def simple_aes_encrypt(msg,key):
#     assert len(key) == 32
#     assert len(msg) == 16
#     msg = hexlify(msg) # Stupid hack/workaround for ascii decode errors
#     msg = msg + '7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b7b'
#     cipher = AES.new(key)
#     return cipher.encrypt(unhexlify(msg))[:16]
#
# def simple_aes_decrypt(msg,key):
#     assert len(msg) == 16
#     assert len(key) == 32
#     cipher = AES.new(key)
#     msg = hexlify(cipher.decrypt(msg))
#     while msg[-2:] == '7b': # Can't use rstrip for multiple chars
#         msg = msg[:-2]
#     for i in range((32 - len(msg))//2):
#         msg = msg + '7b'
#     assert len(msg) == 32
#     return unhexlify(msg)
#
# def passphrase_to_key(intermediatecode,iscompressed=False, seedb = hashlib.sha256(hashlib.sha256(os.urandom(40)).digest()).digest()[:24]):
#
#     # intermediatecode = normalize_input(intermediatecode)
#
#     assert intermediatecode[:10] == 'passphrase'
#     intermediatecode = decode(intermediatecode)
#     assert intermediatecode[:4] == '2ce9'
#     assert len(intermediatecode) == 98
#     assert intermediatecode[14:16] == '51' or intermediatecode[14:16] == '53'
#     prefix = '0143' # Using EC multiplication
#     if iscompressed:
#         flagbyte = 32
#     else:
#         flagbyte = 0
#     magicbytes = intermediatecode[:16]
#     owner_entropy = intermediatecode[16:32]
#     passpoint = intermediatecode[32:]
#     if intermediatecode[14:16] == '51':
#         flagbyte += 4
#     flagbyte = integer_to_bytes(flagbyte)
#     seedb = hexlify(seedb)
#     factorb = sha256(seedb)
#     assert int(factorb,16) > 0 and int(factorb,16) < N
#         # Use a new seedb if this assertion fails
#         # It is just random horrendously bad luck if this happens.
#     newkey = multiplypub(passpoint,factorb,iscompressed)
#     address = pubtoaddress(newkey,'00')
#     try: addrhex = hexlify(address)
#     except: addrhex = hexlify(bytearray(address,'ascii'))
#     addresshash = sha256(addrhex)[:8]
#     salt = unhexlify(addresshash + owner_entropy)
#     passpoint = unhexlify(passpoint)
#     scrypthash = hexlify(scrypt.hash(passpoint,salt,1024,1,1,64))
#     msg1 = integer_to_bytes(int(seedb[:32],16) ^ int(scrypthash[:32],16),16)
#     key = unhexlify(scrypthash[64:])
#     half1 = hexlify(simple_aes_encrypt(unhexlify(msg1),key))
#     msg2 = integer_to_bytes(int(half1[16:] + seedb[32:],16) ^ int(scrypthash[32:64],16),16)
#     half2 = hexlify(simple_aes_encrypt(unhexlify(msg2),key))
#     enckey = ensure_string(encode(get_bytes(prefix + flagbyte.hex() + addresshash.hex() + owner_entropy + half1[:16].hex() + half2.hex())))
#
#     pointb = private_key_to_public_key(factorb, "compressed")
#     pointb_prefix = (int(scrypthash[126:],16) & 1) ^ int(pointb[:2],16)
#     pointb_prefix = integer_to_bytes(pointb_prefix)
#     msg3 = int(pointb[2:34],16) ^ int(scrypthash[:32],16)
#     msg4 = int(pointb[34:],16) ^ int(scrypthash[32:64],16)
#     msg3 = unhexlify(integer_to_bytes(msg3,16))
#     msg4 = unhexlify(integer_to_bytes(msg4,16))
#     pointb_half1 = hexlify(simple_aes_encrypt(msg3,key))
#     pointb_half2 = hexlify(simple_aes_encrypt(msg4,key))
#     encpointb = pointb_prefix + pointb_half1 + pointb_half2
#     cfrm38code = ensure_string(encode(get_bytes('643bf6a89a' + flagbyte.hex() + addresshash.hex() + owner_entropy + encpointb.hex())))
#     return enckey, cfrm38code, address
#

if __name__ == "__main__":

    PRIVATE_KEY = "cbf4b9f70470856bb4f40f80b87edb90865997ffee6df315ab166d713af433a5"
    # PRIVATE_KEY = "A43A940577F4E97F5C4D39EB14FF083A98187C64EA7C99EF7CE460833959A519"

    UNCOMPRESSED_PRIVATE_KEY = private_key_to_public_key(PRIVATE_KEY, "uncompressed")
    COMPRESSED_PRIVATE_KEY = private_key_to_public_key(PRIVATE_KEY, "compressed")

    print("Uncompressed Public Key:", UNCOMPRESSED_PRIVATE_KEY, public_key_to_addresses(public_key=UNCOMPRESSED_PRIVATE_KEY))
    print("Compressed Public Key:", COMPRESSED_PRIVATE_KEY, public_key_to_addresses(public_key=COMPRESSED_PRIVATE_KEY))

    WIF = private_key_to_wif(private_key=PRIVATE_KEY, wif_type="wif")
    WIF_COMPRESSED = private_key_to_wif(private_key=PRIVATE_KEY, wif_type="wif-compressed")

    print(
        "WIF:", WIF,
        get_wif_type(wif=WIF),
        wif_to_private_key(wif=WIF),
        get_wif_checksum(wif=WIF)
    )
    print(
        "WIF Compressed:", WIF_COMPRESSED,
        get_wif_type(wif=WIF_COMPRESSED),
        wif_to_private_key(wif=WIF_COMPRESSED),
        get_wif_checksum(wif=WIF_COMPRESSED)
    )

    print(bip38_encrypt(wif=WIF, passphrase="TestingOneTwoThree"), "6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg")
    # print(bip38_encrypt(wif=WIF_COMPRESSED, passphrase="TestingOneTwoThree"), "6PYNKZ1EAgYgmQfmNVamxyXVWHzK5s6DGhwP4J5o44cvXdoY7sRzhtpUeo")

    # ic = intermediate_code("TestingOneTwoThree", True)
    # print(ic)
    # print(passphrase_to_key(ic))
    #
    # print(bip38_decrypt("6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg"))
