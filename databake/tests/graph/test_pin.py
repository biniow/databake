#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from databake.lib.graph.pin import Pin, INPUT_PIN, OUTPUT_PIN


class TestPin(TestCase):
    def test_pin_createEmptyObject_objectProperlyCreated(self):
        # Arrange/Act
        node = None
        pin_name = 'pin1'
        pin = Pin(node, pin_name, INPUT_PIN)

        # Assert
        self.assertEqual(pin.node, node)
        self.assertEqual(pin.name, pin_name)
        self.assertEqual(pin.type, INPUT_PIN)

    def test_eq_theSameObjectsComparison_returnTrue(self):
        # Arrange
        pin1 = Pin(None, 'pin1', INPUT_PIN)
        pin2 = Pin(None, 'pin1', INPUT_PIN)

        # Act
        result = pin1 == pin2

        # Assert
        self.assertTrue(result)

    def test_eq_differentObjectsComparison_returnFalse(self):
        # Arrange
        pin1 = Pin(None, 'pin1', INPUT_PIN)
        pin2 = Pin(None, 'pin1', OUTPUT_PIN)

        # Act
        result = pin1 == pin2

        # Assert
        self.assertFalse(result)

