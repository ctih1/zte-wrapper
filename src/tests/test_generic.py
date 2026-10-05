from zte_wrapper.helpers import (
    utf_16_decode,
    utf_16_encode,
    get_zte_timestring,
    parse_zte_timestring,
)
import logging

logger = logging.getLogger("zte")


def test_utf_16_be_encoding():
    assert utf_16_decode(utf_16_encode("hello")) == "hello"


def test_timestring():
    logger.info(get_zte_timestring(0))
    logger.info(parse_zte_timestring("26;10;5;23;16;7;+0"))
