from zte_wrapper.helpers import utf_16_encode, utf_16_decode


def test_utf_16_be_encoding():
    assert utf_16_decode(utf_16_encode("hello")) == "hello"
