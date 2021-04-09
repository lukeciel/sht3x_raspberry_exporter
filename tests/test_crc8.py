from sht3x_raspberry_exporter.sht3x import _crc8

def test_crc8():
    assert _crc8(0xBE, 0xEF, 0x92)