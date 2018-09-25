# -*- coding: utf-8 -*-

import gc
import pyb

class WS2812:
    """
    Driver for WS2812 RGB LEDs. May be used for controlling single LED or chain
    of LEDs.

    Version: 1.0
    """

    buf_bytes = (0x11, 0x13, 0x31, 0x33)
    c_red = (255, 0, 0)
    c_green = (0, 255, 0)
    c_blue = (0, 0, 255)
    c_yellow = (255, 255, 0)
    c_pink = (255, 20, 147)
    c_white = (85, 85, 85)
    c_off = (0, 0, 0)
    c_colors = {0:c_off, 1:c_green, 2:c_blue, 3:c_yellow, 4:c_pink, 5:c_red}

    def __init__(self, spi_bus=1, intensity=1):
        """
        Params:
        * spi_bus = SPI bus ID (1 or 2)
        * led_count = count of LEDs
        * intensity = light intensity (float up to 1)
        """

        self.color_stop = self.c_red
        self.color_headlight = self.c_white
        self.color_directional = self.c_yellow

        self.headlights = False
        self.stops = False
        self.direction_r = False
        self.direction_l = False
        self.state = 0
        self.id = 0


        self.led_count = 9
        self.intensity = intensity

        # prepare SPI data buffer (4 bytes for each color)
        self.buf_length = self.led_count * 3 * 4
        self.buf = bytearray(self.buf_length)

        # SPI init
        self.spi = pyb.SPI(spi_bus, pyb.SPI.MASTER, baudrate=3200000, polarity=0, phase=1)

        # turn LEDs off
        #self.show([])
        self.show()

    def show(self):
        """
        Show RGB data on LEDs. Expected data = [(R, G, B), ...] where R, G and B
        are intensities of colors in range from 0 to 255. One RGB tuple for each
        LED. Count of tuples may be less than count of connected LEDs.
        """

        c_stops = self.c_off
        c_headlights = self.c_off
        c_direction_r = self.c_off
        c_direction_l = self.c_off
        c_state = self.c_off
        c_id = self.c_off

        if self.headlights:
        	c_headlights = self.color_headlight

        if self.stops:
        	c_stops = self.color_stop

        if self.direction_r:
            c_direction_r = self.color_directional

        if self.direction_l:
            c_direction_l = self.color_directional

        data = [c_headlights, c_headlights, c_stops, c_stops, c_direction_r, c_direction_l, self.c_colors[self.state], self.c_colors[self.id], self.c_off]
        #print(data)

        self.fill_buf(data)
        self.send_buf()

    def send_buf(self):
        """
        Send buffer over SPI.
        """
        self.spi.send(self.buf)
        gc.collect()

    def update_buf(self, data, start=0):
        """
        Fill a part of the buffer with RGB data.

        Order of colors in buffer is changed from RGB to GRB because WS2812 LED
        has GRB order of colors. Each color is represented by 4 bytes in buffer
        (1 byte for each 2 bits).

        Returns the index of the first unfilled LED

        Note: If you find this function ugly, it's because speed optimisations
        beated purity of code.
        """

        buf = self.buf
        buf_bytes = self.buf_bytes
        intensity = self.intensity

        mask = 0x03
        index = start * 12
        for red, green, blue in data:
            red = int(red * intensity)
            green = int(green * intensity)
            blue = int(blue * intensity)

            buf[index] = buf_bytes[green >> 6 & mask]
            buf[index+1] = buf_bytes[green >> 4 & mask]
            buf[index+2] = buf_bytes[green >> 2 & mask]
            buf[index+3] = buf_bytes[green & mask]

            buf[index+4] = buf_bytes[red >> 6 & mask]
            buf[index+5] = buf_bytes[red >> 4 & mask]
            buf[index+6] = buf_bytes[red >> 2 & mask]
            buf[index+7] = buf_bytes[red & mask]

            buf[index+8] = buf_bytes[blue >> 6 & mask]
            buf[index+9] = buf_bytes[blue >> 4 & mask]
            buf[index+10] = buf_bytes[blue >> 2 & mask]
            buf[index+11] = buf_bytes[blue & mask]

            index += 12

        return index // 12

    def fill_buf(self, data):
        """
        Fill buffer with RGB data.

        All LEDs after the data are turned off.
        """
        end = self.update_buf(data)

        # turn off the rest of the LEDs
        buf = self.buf
        off = self.buf_bytes[0]
        for index in range(end * 12, self.buf_length):
            buf[index] = off
            index += 1
