import time
import smbus


__all__ = ["CRCError", "read_temperature_and_humidity"]


class CRCError(Exception):
    """ Exception raised when the CRC check on the SHT3x data fails. """
    ...


def _crc8(msb, lsb, crc):
    hash = 0xFF
    hash ^= msb

    for i in range(8):
        if (hash & 0x80) != 0:
            hash = (hash << 1) ^ 0x31
        else:
            hash <<= 1
    
    hash ^= lsb
    for i in range(8):
        if (hash & 0x80) != 0:
            hash = (hash << 1) ^ 0x31
        else:
            hash <<= 1
    
    return (hash & 0xFF) == crc
    

def read_temperature_and_humidity(bus: smbus.SMBus, sleep=0.2, crc_check=True):
    """ Reads the temperature and humidity from the specifield bus.

    Parameters
    ----------
    bus: smbus.SMBus
        The :class:`smbus.SMBus` to use.
    sleep: float
        The time in seconds to sleep between sending the measure data command
        to the SHT3x and retrieving the data. Usually, 0.2 seconds should be
        enough, but it can set to a higher value in case of errors.
    crc_check: boolean
        If set to true (default), the function will perform a CRC check on the
        data received from the sensor. If set to false, the check will be
        skipped.
    """

    bus.write_i2c_block_data(0x44, 0x2C, [0x06])
    time.sleep(sleep)

    data = bus.read_i2c_block_data(0x44, 0x0, 6)
    temperature = (data[0] << 8) + data[1]
    crc_temperature = data[2]
    humidity = (data[3] << 8) + data[4]
    crc_humidity = data[5]

    if crc_check:
        crc_valid = (
            _crc8(data[0], data[1], data[2]),
            _crc8(data[3], data[4], data[5])
        )

        if not all(crc_valid):
            raise CRCError()

    real_temperature = -45 + 175 * (temperature / 65535.0)
    real_humidity = 100 * humidity / 65535.0

    return real_temperature, real_humidity


if __name__ == "__main__":
    bus = smbus.SMBus(1)
    temp, humidity = read_temperature_and_humidity(bus)

    print("{:.2f}°C, {:.2f}% RH".format(temp, humidity))