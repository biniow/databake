#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from databake.lib.graph.exceptions import InvalidPinTypeError
from databake.lib.graph.node import Node
from databake.lib.graph.pin import Pin, INPUT_PIN, OUTPUT_PIN


class TestPin(TestCase):
    def test_pin_createEmptyObject_objectProperlyCreated(self):
        # Arrange/Act
        pin_name = 'pin1'
        pin = Pin(pin_name, INPUT_PIN)
        pin.node = None

        # Assert
        self.assertEqual(pin.node, None)
        self.assertEqual(pin.name, pin_name)
        self.assertEqual(pin.type, INPUT_PIN)

    def test_pin_addPinWithNoValidType_raiseException(self):
        # Arrange
        pin_name = 'pin1'
        pin_type = 'not_valid'

        # Act/Assert
        self.assertRaises(InvalidPinTypeError, Pin, pin_name, pin_type)

    def test_eq_theSameObjectsComparison_returnTrue(self):
        # Arrange
        pin1 = Pin('pin1', INPUT_PIN)
        pin2 = Pin('pin1', INPUT_PIN)

        # Act
        result = pin1 == pin2

        # Assert
        self.assertTrue(result)

    def test_eq_differentObjectsComparison_returnFalse(self):
        # Arrange
        pin1 = Pin('pin1', INPUT_PIN)
        pin2 = Pin('pin1', OUTPUT_PIN)

        # Act
        result = pin1 == pin2

        # Assert
        self.assertFalse(result)