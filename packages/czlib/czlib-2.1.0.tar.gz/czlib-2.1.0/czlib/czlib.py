import io
import os
import zlib
from dataclasses import dataclass
from typing import BinaryIO

from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA1

HASH_SIZE = 20  # size of hash value in bytes
BLOCK_SIZE = AES.block_size  # size of AES block in bytes
KEY_SIZE = 32  # size of AES key in bytes
AES_MODE = AES.MODE_CBC  # cipher block chaining
CHUNK_SIZE = 2 ** 27  # 128 MB # chunk size to read from io in bytes
SALT_SIZE = 32  # size of salt

assert BLOCK_SIZE == 16
assert CHUNK_SIZE % BLOCK_SIZE == 0


def sha1_hash(f_in: BinaryIO) -> bytes:
    h = SHA1.new()
    while True:
        chunk = f_in.read(CHUNK_SIZE)
        if len(chunk) == 0:
            b = h.digest()
            assert len(b) == HASH_SIZE
            return b
        h.update(chunk)


def read_compress_encrypt_write(
        key: bytes, init_vec: bytes,
        plain_read_io: BinaryIO, encrypted_write_io: BinaryIO,
):
    assert len(init_vec) == BLOCK_SIZE
    assert len(key) == KEY_SIZE

    c = AES.new(key, AES_MODE, init_vec)
    z = zlib.compressobj(level=zlib.Z_BEST_COMPRESSION, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS, memLevel=9)
    b = b""

    def read_compress(b: bytes) -> tuple[bytes, bool]:
        while len(b) < BLOCK_SIZE:
            chunk = plain_read_io.read(CHUNK_SIZE)
            if len(chunk) == 0:
                b += z.flush()
                return b, True
            b += z.compress(chunk)
        return b, False

    def encrypt_write(b: bytes, eof: bool) -> bytes:
        if eof:
            # pad 0s until multiples of BLOCK_SIZE
            pad = (BLOCK_SIZE - len(b) % BLOCK_SIZE)
            chunk, b = b + b"\0" * pad, b""
        else:
            # take the maximum multiples of BLOCK SIZE
            bound = (len(b) // BLOCK_SIZE) * BLOCK_SIZE
            chunk, b = b[:bound], b[bound:]

        encrypted_chunk = c.encrypt(chunk)
        encrypted_write_io.write(encrypted_chunk)
        return b

    eof = False
    while not eof:
        b, eof = read_compress(b)
        b = encrypt_write(b, eof)


def read_decrypt_decompress_write(
        key: bytes, init_vec: bytes, file_size: int,
        encrypted_read_io: BinaryIO, decrypted_write_io: BinaryIO,
):
    assert len(init_vec) == BLOCK_SIZE
    assert len(key) == KEY_SIZE

    c = AES.new(key, AES_MODE, init_vec)
    z = zlib.decompressobj(wbits=zlib.MAX_WBITS)

    def read_decrypt_decompress() -> tuple[bytes, bool]:
        encrypted_chunk = encrypted_read_io.read(CHUNK_SIZE)
        if len(encrypted_chunk) == 0:
            return b"", True
        chunk = c.decrypt(encrypted_chunk)
        b = z.decompress(chunk)
        return b, False

    eof = False
    remaining_size = file_size
    while not eof and remaining_size > 0:
        b, eof = read_decrypt_decompress()
        if eof:
            b += z.flush()

        if remaining_size < len(b):
            b = b[:remaining_size]
        remaining_size -= len(b)
        decrypted_write_io.write(b)


def make_key_from_passphrase(passphrase: bytes) -> bytes:
    hash = sha1_hash(io.BytesIO(passphrase))
    hash += hash * (KEY_SIZE // HASH_SIZE)
    key = hash[:KEY_SIZE]
    return key


@dataclass
class Certificate:
    salt: bytes
    key_sig: bytes


def verify_certificate(cert: Certificate, passphrase: bytes) -> bytes:
    passphrase_with_salt = cert.salt + passphrase
    key = make_key_from_passphrase(passphrase_with_salt)
    key_hash = sha1_hash(io.BytesIO(key))
    assert key_hash == cert.key_sig, "passphrase_does_not_match"
    return key


def make_certificate(passphrase: bytes) -> Certificate:
    salt = os.urandom(SALT_SIZE)
    passphrase_with_salt = salt + passphrase
    key = make_key_from_passphrase(passphrase_with_salt)
    key_hash = sha1_hash(io.BytesIO(key))
    return Certificate(salt=salt, key_sig=key_hash)
