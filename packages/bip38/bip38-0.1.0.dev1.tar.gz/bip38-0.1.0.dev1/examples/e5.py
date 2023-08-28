#!/usr/bin/env python3

from typing import (
    Tuple, Union, Optional
)
from pyaes import AESModeOfOperationECB

import scrypt
import unicodedata
import os

try:
    from typing import Literal  # pylint: disable=unused-import
except ImportError:
    # Literal not supported by Python 3.7
    from typing_extensions import Literal  # type: ignore # noqa: F401

from bip38.utils import (
    integer_to_bytes, bytes_to_integer, get_bytes, double_sha256, hash160, get_hex_string
)
from bip38.libs.base58 import (
    encode, decode, ensure_string
)

# Address prefix
ADDRESS_PREFIX: int = 0x00
# Wallet important format prefix
WIF_PREFIX: int = 0x80
# BIP38 non-EC-multiplied private key prefix
BIP38_NON_EC_PRIVATE_KEY_PREFIX: int = 0x0142
# BIP38 EC-multiplied private key prefix
BIP38_EC_PRIVATE_KEY_PREFIX: int = 0x0143
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
# Checksum byte length
CHECKSUM_BYTE_LENGTH: int = 4
# Private key prefixes
UNCOMPRESSED_PRIVATE_KEY_PREFIX: int = 0x00
COMPRESSED_PRIVATE_KEY_PREFIX: int = 0x01
# Public key prefixes
EVEN_COMPRESSED_PUBLIC_KEY_PREFIX: int = 0x02
ODD_COMPRESSED_PUBLIC_KEY_PREFIX: int = 0x03
UNCOMPRESSED_PUBLIC_KEY_PREFIX: int = 0x04
# Wallet important format flag
WIF_FLAG: int = 0xc0
# Wallet important format compressed flag
WIF_COMPRESSED_FLAG: int = 0xe0


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


def multiply_private_key(p1: bytes, p2: bytes) -> bytes:
    return integer_to_bytes((bytes_to_integer(p1) * bytes_to_integer(p2)) % N)


def private_key_to_public_key(private_key: Union[str, bytes], public_key_type: Literal["uncompressed", "compressed"] = "compressed") -> str:
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
    return double_sha256(raw)[:CHECKSUM_BYTE_LENGTH]


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


def private_key_to_wif(private_key: Union[str, bytes], wif_type: Literal["wif", "wif-compressed"] = "wif-compressed") -> str:
    # Getting uncompressed and compressed
    wif, wif_compressed = encode_wif(private_key=private_key)

    if wif_type == "wif":
        return wif
    elif wif_type == "wif-compressed":
        return wif_compressed
    else:
        raise ValueError("Invalid WIF type, choose only 'uncompressed' or 'compressed' types")


def decode_wif(wif: str) -> Tuple[bytes, Literal["wif", "wif-compressed"], bytes]:
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
    wif_type: Literal["wif", "wif-compressed"] = "wif"

    if len(private_key) not in [33, 32]:
        raise ValueError(f"Invalid wallet important format")
    elif len(private_key) == 33:
        private_key = private_key[:-len(integer_to_bytes(COMPRESSED_PRIVATE_KEY_PREFIX))]
        wif_type = "wif-compressed"

    return private_key, wif_type, checksum


def wif_to_private_key(wif: str) -> str:
    return get_hex_string(decode_wif(wif=wif)[0])


def get_wif_type(wif: str) -> Literal["wif", "wif-compressed"]:
    return decode_wif(wif=wif)[1]


def get_wif_checksum(wif: str) -> str:
    return get_hex_string(decode_wif(wif=wif)[2])


def public_key_to_addresses(public_key: Union[str, bytes]) -> str:
    # Getting public key hash
    public_key_hash: bytes = hash160(get_bytes(public_key))
    payload: bytes = (
        integer_to_bytes(ADDRESS_PREFIX) + public_key_hash
    )
    return ensure_string(encode(payload + get_checksum(payload)))


def bip38_encrypt(wif: str, passphrase: str) -> str:

    wif_type: Literal["wif", "wif-compressed"] = get_wif_type(wif=wif)
    if wif_type == "wif":
        flag: bytes = integer_to_bytes(WIF_FLAG)
        private_key: str = wif_to_private_key(wif=wif)
        public_key_type: Literal["uncompressed", "compressed"] = "uncompressed"
    elif wif_type == "wif-compressed":
        flag: bytes = integer_to_bytes(WIF_COMPRESSED_FLAG)
        private_key: str = wif_to_private_key(wif=wif)
        public_key_type: Literal["uncompressed", "compressed"] = "compressed"
    else:
        raise ValueError("Wrong wallet important format type")

    public_key: str = private_key_to_public_key(
        private_key=private_key, public_key_type=public_key_type
    )
    address: str = public_key_to_addresses(public_key=public_key)
    address_hash: bytes = get_checksum(get_bytes(address, unhexlify=False))
    key: bytes = scrypt.hash(unicodedata.normalize('NFC', passphrase), address_hash, 16384, 8, 8)
    derived_half_1, derived_half_2 = key[0:32], key[32:64]

    aes: AESModeOfOperationECB = AESModeOfOperationECB(derived_half_2)
    encrypted_half_1: bytes = aes.encrypt(integer_to_bytes(
        bytes_to_integer(get_bytes(private_key[0:32])) ^ bytes_to_integer(derived_half_1[0:16])
    ))
    encrypted_half_2: bytes = aes.encrypt(integer_to_bytes(
        bytes_to_integer(get_bytes(private_key[32:64])) ^ bytes_to_integer(derived_half_1[16:32])
    ))

    encrypted_privkey: bytes = (
        integer_to_bytes(BIP38_NON_EC_PRIVATE_KEY_PREFIX) + flag + address_hash + encrypted_half_1 + encrypted_half_2
    )
    return ensure_string(encode(
        encrypted_privkey + get_checksum(encrypted_privkey)
    ))


COMPRESSION_FLAG_BYTES = ['20', '24', '28', '2c', '30', '34', '38', '3c', 'e0', 'e8', 'f0', 'f8']
LOT_SEQUENCE_FLAG_BYTES = ['04', '0c', '14', '1c', '24', '2c', '34', '3c']
NON_MULTIPLIED_FLAG_BYTES = ['c0', 'c8', 'd0', 'd8', 'e0', 'e8', 'f0', 'f8']
EC_MULTIPLIED_FLAG_BYTES = ['00', '04', '08', '0c', '10', '14', '18', '1c', '20', '24', '28', '2c', '30', '34', '38', '3c']
ILLEGAL_FLAG_BYTES = ['c4', 'cc', 'd4', 'dc', 'e4', 'ec', 'f4', 'fc']


def bip38_decrypt(encrypted_wif: str, passphrase: str, detail: bool = False) -> Union[str, dict]:

    encrypted_wif_decode: bytes = decode(encrypted_wif)
    if len(encrypted_wif_decode) != 43:
        raise ValueError(f"Invalid encrypted WIF (expected 43, got {len(encrypted_wif_decode)!r})")

    prefix: bytes = encrypted_wif_decode[:2]
    if prefix == integer_to_bytes(BIP38_NON_EC_PRIVATE_KEY_PREFIX):

        flag: bytes = encrypted_wif_decode[2:3]
        if flag == integer_to_bytes(WIF_FLAG):
            wif_type: Literal["wif", "wif-compressed"] = "wif"
            public_key_type: Literal["uncompressed", "compressed"] = "uncompressed"
        elif flag == integer_to_bytes(WIF_COMPRESSED_FLAG):
            wif_type: Literal["wif", "wif-compressed"] = "wif-compressed"
            public_key_type: Literal["uncompressed", "compressed"] = "compressed"
        else:
            raise ValueError(
                f"Invalid flag (expected {get_hex_string(integer_to_bytes(WIF_FLAG))!r} or "
                f"{get_hex_string(integer_to_bytes(WIF_COMPRESSED_FLAG))!r}, got {get_hex_string(flag)!r})"
            )

        address_hash: bytes = encrypted_wif_decode[3:7]
        key: bytes = scrypt.hash(unicodedata.normalize('NFC', passphrase), address_hash, 16384, 8, 8)
        derived_half_1, derived_half_2 = key[0:32], key[32:64]
        encrypted_half_1: bytes = encrypted_wif_decode[7:23]
        encrypted_half_2: bytes = encrypted_wif_decode[23:39]

        aes: AESModeOfOperationECB = AESModeOfOperationECB(derived_half_2)
        decrypted_half_2: bytes = aes.decrypt(encrypted_half_2)
        decrypted_half_1: bytes = aes.decrypt(encrypted_half_1)

        private_key: bytes = integer_to_bytes(
            bytes_to_integer(decrypted_half_1 + decrypted_half_2) ^ bytes_to_integer(derived_half_1)
        )
        if bytes_to_integer(private_key) == 0 or bytes_to_integer(private_key) >= N:
            raise ValueError("Invalid ec encrypted wallet important format")

        public_key: str = private_key_to_public_key(
            private_key=private_key, public_key_type=public_key_type
        )
        address: str = public_key_to_addresses(public_key=public_key)
        if get_checksum(get_bytes(address, unhexlify=False)) != address_hash:
            raise ValueError("Incorrect passphrase or password")

        return private_key_to_wif(
            private_key=private_key, wif_type=wif_type
        )

    elif prefix == integer_to_bytes(BIP38_EC_PRIVATE_KEY_PREFIX):

        flag: bytes = encrypted_wif_decode[2:3]
        owner_entropy: bytes = encrypted_wif_decode[7:15]
        encrypted_half_1_half_1: bytes = encrypted_wif_decode[15:23]
        encrypted_half_2: bytes = encrypted_wif_decode[23:-4]

        if flag.hex() in LOT_SEQUENCE_FLAG_BYTES:
            lot_sequence = owner_entropy[4:]
            owner_salt = owner_entropy[:4]
        else:
            lot_sequence = False
            owner_salt = owner_entropy

        pre_private_key: bytes = scrypt.hash(unicodedata.normalize('NFC', passphrase), owner_salt, 16384, 8, 8, 32)
        if lot_sequence:
            pre_private_key: bytes = double_sha256(pre_private_key + owner_entropy)
        if bytes_to_integer(pre_private_key) == 0 or bytes_to_integer(pre_private_key) >= N:
            raise ValueError("Invalid ec encrypted wallet important format")

        pre_public_key: str = private_key_to_public_key(
            private_key=pre_private_key, public_key_type="compressed"
        )
        salt = encrypted_wif_decode[3:7] + owner_entropy
        encrypted_seedb: bytes = scrypt.hash(get_bytes(pre_public_key), salt, 1024, 1, 1, 64)
        key: bytes = encrypted_seedb[32:]

        aes: AESModeOfOperationECB = AESModeOfOperationECB(key)
        encrypted_half_1_half_2_seedb_last_3 = integer_to_bytes(
            bytes_to_integer(aes.decrypt(encrypted_half_2)) ^ bytes_to_integer(encrypted_seedb[16:32])
        )
        encrypted_half_1_half_2: bytes = encrypted_half_1_half_2_seedb_last_3[:8]
        encrypted_half_1: bytes = (
            encrypted_half_1_half_1 + encrypted_half_1_half_2
        )

        seedb: bytes = integer_to_bytes(
            bytes_to_integer(aes.decrypt(encrypted_half_1)) ^ bytes_to_integer(encrypted_seedb[:16])
        ) + encrypted_half_1_half_2_seedb_last_3[8:]

        factor_b: bytes = double_sha256(seedb)
        if bytes_to_integer(factor_b) == 0 or bytes_to_integer(factor_b) >= N:
            raise ValueError("Invalid ec encrypted wallet important format")

        private_key: bytes = multiply_private_key(pre_private_key, factor_b)
        if flag in COMPRESSION_FLAG_BYTES:
            wif_type = "wif-compressed"
            public_key_type = "compressed"
        else:
            wif_type = "wif"
            public_key_type = "uncompressed"
        public_key: str = private_key_to_public_key(
            private_key=private_key, public_key_type=public_key_type
        )
        address: str = public_key_to_addresses(public_key=public_key)
        if get_checksum(get_bytes(address, unhexlify=False)) == encrypted_wif_decode[3:7]:
            wif: str = private_key_to_wif(
                private_key=private_key, wif_type=wif_type
            )
            lot: Optional[int] = None
            sequence: Optional[int] = None
            if detail:
                if lot_sequence:
                    sequence_lot: int = bytes_to_integer(lot_sequence)
                    sequence: int = sequence_lot % 4096
                    lot: int = (sequence_lot - sequence) // 4096
                return dict(
                    wif=wif,
                    private_key=get_hex_string(private_key),
                    wif_type=wif_type,
                    public_key=public_key,
                    public_key_type=public_key_type,
                    address=address,
                    lot=lot,
                    sequence=sequence
                )
            return wif
        raise ValueError("Incorrect passphrase or password")
    else:
        raise ValueError(
            f"Invalid prefix (expected {get_hex_string(integer_to_bytes(BIP38_NON_EC_PRIVATE_KEY_PREFIX))!r} or "
            f"{get_hex_string(integer_to_bytes(BIP38_EC_PRIVATE_KEY_PREFIX))!r}, got {get_hex_string(prefix)!r})"
        )


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
    print(bip38_encrypt(wif=WIF_COMPRESSED, passphrase="TestingOneTwoThree"), "6PYNKZ1EAgYgmQfmNVamxyXVWHzK5s6DGhwP4J5o44cvXdoY7sRzhtpUeo")

    print(bip38_decrypt(encrypted_wif="6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg", passphrase="TestingOneTwoThree"))
    print(bip38_decrypt(encrypted_wif="6PYNKZ1EAgYgmQfmNVamxyXVWHzK5s6DGhwP4J5o44cvXdoY7sRzhtpUeo", passphrase="TestingOneTwoThree"))

    print(bip38_decrypt(encrypted_wif="6PfQu77ygVyJLZjfvMLyhLMQbYnu5uguoJJ4kMCLqWwPEdfpwANVS76gTX", passphrase="TestingOneTwoThree", detail=True))
    print(bip38_decrypt(encrypted_wif="6PgNBNNzDkKdhkT6uJntUXwwzQV8Rr2tZcbkDcuC9DZRsS6AtHts4Ypo1j", passphrase="MOLON LABE", detail=True))

# c3980b33a727ab5f28086b51c7ec4bb1baa6307fb84380cac91939ea29f9b64b
