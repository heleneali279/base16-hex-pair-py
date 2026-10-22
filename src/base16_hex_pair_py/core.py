import binascii


def encode(data: bytes) -> str:
    """Encode bytes to a lowercase hex string.

    Uses binascii.hexlify for its native C implementation. Lowercase is
    chosen because it matches the output of most hex tools and avoids
    ambiguity in environments that normalize letter case.

    Args:
        data: The bytes to encode.

    Returns:
        The hex string for the given bytes, where each byte becomes
        exactly two characters. An empty bytes object produces an empty
        string.
    """
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("data must be bytes-like")
    return binascii.hexlify(data).decode("ascii")


def decode(text: str) -> bytes:
    """Decode a hex string to bytes.

    Decoding accepts only strings that, after stripping all
    whitespace, contain zero or more complete hex pairs. A 'hex pair'
    is two characters from the set [0-9a-fA-F].

    Design decisions:
      * Lowercase and uppercase hex digits are both accepted. This is
        a decoding function; rejecting uppercase would surprise users
        who paste hex from other tools. The encode function emits
        lowercase, so the two are lossless round-trips.
      * Whitespace is ignored (spaces, tabs, newlines, carriage
        returns, form feeds, and vertical tabs) so that hex dumps with
        line breaks or column separators can be decoded without a
        preprocessing step. A leading/trailing space won't cause an
        error.
      * An odd number of hex digits after stripping whitespace is an
        error. We do not guess a missing leading zero; silently
        padding could corrupt the output when the user intended a
        specific value.
      * Non-hex characters (anything outside [0-9a-fA-F] that isn't
        whitespace) are an error. The library refuses to return
        partial or corrupted data.

    Args:
        text: The hex string to decode.

    Returns:
        The decoded bytes. An empty string (or an all-whitespace
        string) produces an empty bytes object.

    Raises:
        TypeError: If text is not a str.
        ValueError: If text contains non-hex, non-whitespace
            characters, or if it contains an odd number of hex digits
            after stripping whitespace.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")

    compact = "".join(text.split())

    if len(compact) % 2 != 0:
        raise ValueError(
            "odd-length hex string: {} digits after stripping whitespace".format(
                len(compact)
            )
        )

    if compact:
        return binascii.unhexlify(compact)
    return b""
