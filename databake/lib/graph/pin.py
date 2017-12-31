#!/usr/bin/env python
# -*- coding: utf-8 -*-

INPUT_PIN, OUTPUT_PIN = 1, 2
PIN_TYPES = (INPUT_PIN, OUTPUT_PIN)


class Pin:
    def __init__(self, node, name, pin_type):
        self.node = node
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

