#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.graph.exceptions import PinConnectionError
from databake.lib.graph.pin import OUTPUT_PIN, INPUT_PIN


class Connection:
    def __init__(self, from_pin, to_pin, comment=None):
        if Connection.is_valid_pin_type_configuration(from_pin, to_pin):
            raise PinConnectionError

        self.from_pin = from_pin
        self.to_pin = to_pin
        self.comment = comment

    @staticmethod
    def is_valid_pin_type_configuration(from_pin, to_pin):
        return (from_pin.type == to_pin.type) or \
               (from_pin.type == OUTPUT_PIN and to_pin.type == INPUT_PIN)
