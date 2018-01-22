#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from databake.lib.graph.connection import Connection
from databake.lib.graph.exceptions import PinConnectionError
from databake.lib.graph.pin import INPUT_PIN, Pin, OUTPUT_PIN


class TestConnection(TestCase):
    def test_connection_objectCreation_correctlyCreated(self):
        # Arrange
        pin1 = Pin('pin1', INPUT_PIN)
        pin2 = Pin('pin2', OUTPUT_PIN)
        comment = 'Dummy connection between pins'

        # Act
        connection = Connection(pin1, pin2, comment)

        # Assert
        self.assertEqual(connection.from_pin, pin1)
        self.assertEqual(connection.to_pin, pin2)
        self.assertEqual(connection.comment, comment)

    def test_connection_pinTypesWrongConfiguration_raisePinConnectionError(self):
        # Arrange
        pin1 = Pin('pin1', INPUT_PIN)
        pin2 = Pin('pin2', INPUT_PIN)
        pin3 = Pin('pin3', OUTPUT_PIN)
        pin4 = Pin('pin4', OUTPUT_PIN)

        # Act / Assert
        self.assertRaises(PinConnectionError, Connection, pin1, pin2)
        self.assertRaises(PinConnectionError, Connection, pin3, pin4)
        self.assertRaises(PinConnectionError, Connection, pin4, pin1)