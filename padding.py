# padding.py
def pad(data):
    """
    Pad the data to be a multiple of 8 bytes (Triple DES block size)
    """
    padding_length = 8 - (len(data) % 8)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad(data):
    """
    Remove the padding from the data
    """
    padding_length = data[-1]
    return data[:-padding_length]