from base64 import b32decode
from base64 import b16encode
from bech32 import bech32_decode
from bech32 import bech32_encode

B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

def add_padding(base32_len):
    bits = base32_len * 5
    padding_size = (8 - (bits % 8)) % 8
    return padding_size

def npub_to_hex(npub):
    hrd, data = bech32_decode(npub)
    b32_data = [B32[index] for index in data]
    data_str = "".join(b32_data)
    data_length = len(data_str)
    data_str += "=" * add_padding(data_length)
    decoded_data = b32decode(data_str)
    b16_encoded_data = b16encode(decoded_data)
    hex_str = b16_encoded_data.decode("utf-8").lower()
    return hex_str

def json(links):
    names = {}
    for link in links:
        names[link['name']] = npub_to_hex(link['pub'])

    return {'names':names}