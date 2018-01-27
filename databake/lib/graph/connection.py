#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.graph.exceptions import PinConnectionError
from databake.lib.graph.pin import OUTPUT_PIN, INPUT_PIN


class Connection:
    def __init__(self, from_pin, to_pin, comment=None):

        Connection.validate_connection(from_pin, to_pin)

        self.from_pin = from_pin
        self.to_pin = to_pin
        self.comment = comment

        if from_pin.node.level == to_pin.node.level:
            to_pin.node.level += 1

    @staticmethod
    def validate_connection(from_pin, to_pin):
        msg = None
        if not Connection._is_valid_pin_type_configuration(from_pin, to_pin):
            msg = f'Only OUTPUT_PIN -> INPUT_PIN connection allowed. {from_pin} -> {to_pin} is not valid'
        elif Connection._is_circular_reference(from_pin, to_pin):
            msg = f'Circular reference detected: {from_pin} -> {to_pin}. Check levels of associated nodes'

        if msg:
            raise PinConnectionError(msg)

    @staticmethod
    def _is_valid_pin_type_configuration(from_pin, to_pin):
        return from_pin.type == OUTPUT_PIN and to_pin.type == INPUT_PIN

    @staticmethod
    def _is_circular_reference(from_pin, to_pin):
        return from_pin.node.level > to_pin.node.level
