import io
import os
import zlib
from dataclasses import dataclass
from typing import BinaryIO

from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA1

from .serialize import uint64_to_bytes, UINT64_SIZE, bytes_to_uint64

HASH_SIZE = 20  # size of hash value in bytes
BLOCK_SIZE = AES.block_size  # size of AES block in bytes
KEY_SIZE = 32  # size of AES key in bytes
AES_MODE = AES.MODE_CBC  # cipher block chaining
CHUNK_SIZE = 2 ** 30  # 1 GB # chunk size to read from io in bytes
SALT_SIZE = 32  # size of salt
COMPRESSION_LEVEL = 9

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


def aes256_encrypt(
        key: bytes, init_vec: bytes,
        plain_read_io: BinaryIO, encrypted_write_io: BinaryIO,
):
    assert len(init_vec) == BLOCK_SIZE
    assert len(key) == KEY_SIZE

    aes = AES.new(key, AES_MODE, init_vec)

    while True:
        # read
        chunk = plain_read_io.read(CHUNK_SIZE)
        if len(chunk) == 0:
            return
        # compress
        compressed_chunk = zlib.compress(chunk, level=COMPRESSION_LEVEL)

        # encrypt
        if len(compressed_chunk) % BLOCK_SIZE != 0:
            # pad 0s until multiples of BLOCK_SIZE
            padded_compressed_chunk = compressed_chunk + b"\0" * (BLOCK_SIZE - len(compressed_chunk) % BLOCK_SIZE)
        else:
            padded_compressed_chunk = compressed_chunk

        encrypted_chunk = aes.encrypt(padded_compressed_chunk)

        # write
        encrypted_write_io.write(
            uint64_to_bytes(len(compressed_chunk)) + uint64_to_bytes(len(encrypted_chunk)) + encrypted_chunk)


def aes256_decrypt(
        key: bytes, init_vec: bytes, file_size: int,
        encrypted_read_io: BinaryIO, decrypted_write_io: BinaryIO,
):
    assert len(init_vec) == BLOCK_SIZE
    assert len(key) == KEY_SIZE

    def read_exact(n: int) -> bytes:
        b = encrypted_read_io.read(n)
        assert len(b) == n, "corrupted_file"
        return b

    aes = AES.new(key, AES_MODE, init_vec)
    remaining_size = file_size
    while remaining_size > 0:
        # read
        len_compressed_chunk = bytes_to_uint64(read_exact(UINT64_SIZE))
        len_encrypted_chunk = bytes_to_uint64(read_exact(UINT64_SIZE))
        encrypted_chunk = read_exact(len_encrypted_chunk)

        # decrypt
        padded_compressed_chunk = aes.decrypt(encrypted_chunk)
        compressed_chunk = padded_compressed_chunk[:len_compressed_chunk]
        # extract
        chunk = zlib.decompress(compressed_chunk)

        if remaining_size < len(chunk):
            chunk = chunk[:remaining_size]
        remaining_size -= len(chunk)

        decrypted_write_io.write(chunk)


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
