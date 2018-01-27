#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.graph.exceptions import InvalidPinTypeError

INPUT_PIN, OUTPUT_PIN = 1, 2


class Pin:
    def __init__(self, name, pin_type):
        if pin_type not in (INPUT_PIN, OUTPUT_PIN):
            raise InvalidPinTypeError

        self.node = None
        self.name = name
        self.type = pin_type

    def __str__(self):
        return f'Pin:{self.name}'

    def __eq__(self, other):
        try:
            assert self.node == other.node
            assert self.name == other.name
            assert self.type == other.type
        except AssertionError:
            return False
        return True