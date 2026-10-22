import binascii
import unittest

from base16_hex_pair_py import encode, decode


class EncodeTests(unittest.TestCase):
    def test_empty_bytes(self):
        self.assertEqual(encode(b""), "")

    def test_single_byte(self):
        self.assertEqual(encode(b"\x00"), "00")
        self.assertEqual(encode(b"\xff"), "ff")
        self.assertEqual(encode(b"\xab"), "ab")

    def test_zero_byte_is_not_dropped(self):
        result = encode(b"\x00")
        self.assertEqual(result, "00")
        self.assertEqual(len(result), 2)

    def test_multiple_bytes(self):
        self.assertEqual(encode(b"Hello, world!"), "48656c6c6f2c20776f726c6421")

    def test_lowercase_output(self):
        for b in [b"\xab", b"\xcd", b"\xef"]:
            self.assertEqual(encode(b), encode(b).lower())

    def test_all_bytes_range(self):
        data = bytes(range(256))
        expected = binascii.hexlify(data).decode("ascii")
        self.assertEqual(encode(data), expected)

    def test_bytearray_input(self):
        self.assertEqual(encode(bytearray(b"\x01\x02")), "0102")

    def test_memoryview_input(self):
        self.assertEqual(encode(memoryview(b"\x03\x04")), "0304")

    def test_rejects_str_input(self):
        with self.assertRaises(TypeError):
            encode("hello")  # type: ignore[arg-type]

    def test_rejects_int_input(self):
        with self.assertRaises(TypeError):
            encode(42)  # type: ignore[arg-type]


class DecodeTests(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(decode(""), b"")

    def test_all_whitespace(self):
        self.assertEqual(decode("   \n\t  "), b"")

    def test_simple_pair(self):
        self.assertEqual(decode("00"), b"\x00")
        self.assertEqual(decode("ff"), b"\xff")

    def test_lowercase_and_uppercase_accepted(self):
        self.assertEqual(decode("4f"), decode("4F"))
        self.assertEqual(decode("ABCD"), b"\xab\xcd")

    def test_mixed_case_accepted(self):
        self.assertEqual(decode("aB"), b"\xab")
        self.assertEqual(decode("AbCd"), b"\xab\xcd")

    def test_ignores_whitespace(self):
        self.assertEqual(decode("48 65 6c 6c 6f"), b"Hello")
        self.assertEqual(decode("48\t65\n6c\r6c\f6f"), b"Hello")
        self.assertEqual(
            decode("\n48\n65\n6c\n6c\n6f\n"),
            b"Hello",
        )

    def test_leading_and_trailing_whitespace(self):
        self.assertEqual(decode("  4865  "), b"He")

    def test_odd_length_raises(self):
        with self.assertRaises(ValueError):
            decode("f")
        with self.assertRaises(ValueError):
            decode("fff")
        with self.assertRaises(ValueError):
            decode("00 f")

    def test_non_hex_characters_raise(self):
        with self.assertRaises(ValueError):
            decode("xy")
        with self.assertRaises(ValueError):
            decode("00gh")
        with self.assertRaises((ValueError, binascii.Error)):
            decode("--")

    def test_rejects_bytes_input(self):
        with self.assertRaises(TypeError):
            decode(b"00ff")  # type: ignore[arg-type]

    def test_rejects_int_input(self):
        with self.assertRaises(TypeError):
            decode(42)  # type: ignore[arg-type]


class RoundTripTests(unittest.TestCase):
    def test_round_trip_all_bytes(self):
        data = bytes(range(256))
        self.assertEqual(decode(encode(data)), data)

    def test_round_trip_with_whitespace(self):
        original = bytes(range(0, 16))
        encoded = encode(original)
        spaced = " ".join(encoded[i : i + 2] for i in range(0, len(encoded), 2))
        self.assertEqual(decode(spaced), original)

    def test_round_trip_empty(self):
        self.assertEqual(decode(encode(b"")), b"")


if __name__ == "__main__":
    unittest.main()
