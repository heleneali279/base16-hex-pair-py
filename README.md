# base16-hex-pair-py

Encodes bytes to a lowercase hexadecimal string and decodes hex pairs back to bytes, ignoring whitespace and validating character ranges.

```python
from base16_hex_pair_py import encode, decode

# bytes -> hex string
print(encode(b"Hi"))   # '4869'

# hex string -> bytes (whitespace ignored, case-insensitive)
print(decode("48 69")) # b'Hi'
print(decode("4F6F"))  # b'Oo'
```

The standard library already offers `binascii.hexlify` and `binascii.unhexlify`, which this library wraps. The value here is the small, strict wrapper: `encode` always emits lowercase hex (two characters per byte, including leading zeros), and `decode` is tolerant of pasted hex dumps that contain spaces, tabs, or line breaks, while still rejecting non-hex characters and odd-length input. If you want raw speed without those guarantees, call `binascii` directly.

The awkward edge: `decode` accepts only strings, not bytes. If you have a hex string as a bytes object (e.g. read from a binary stream), decode it to `str` first. An odd number of hex digits after stripping whitespace raises `ValueError` rather than guessing a missing leading zero — silent padding would be more likely to corrupt data than to help.
