#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from databake.lib.graph.connection import Connection
from databake.lib.graph.exceptions import PinConnectionError
from databake.lib.graph.node import Node
from databake.lib.graph.pin import INPUT_PIN, Pin, OUTPUT_PIN


class TestConnection(TestCase):
    def setUp(self):
        self.node1 = Node(1, 'test', 'Node1')
        self.node1.level = 0
        self.node2 = Node(2, 'test', 'Node2')
        self.node2.level = 1

        self.pin1 = Pin('pin1', OUTPUT_PIN)
        self.pin1.node = self.node1
        self.pin2 = Pin('pin2', OUTPUT_PIN)
        self.pin2.node = self.node2
        self.pin3 = Pin('pin3', INPUT_PIN)
        self.pin3.node = self.node1
        self.pin4 = Pin('pin4', INPUT_PIN)
        self.pin4.node = self.node2

    def test_connection_objectCreation_correctlyCreated(self):
        # Arrange
        comment = 'Dummy connection between pins'

        # Act
        connection = Connection(self.pin1, self.pin4, comment)

        # Assert
        self.assertEqual(connection.from_pin, self.pin1)
        self.assertEqual(connection.to_pin, self.pin4)
        self.assertEqual(connection.comment, comment)

    def test_connection_pinTypesWrongConfiguration_raisePinConnectionError(self):
        # Arrange / Act / Assert
        # Connection the same type pins should raise Exception
        self.assertRaises(PinConnectionError, Connection, self.pin1, self.pin2)
        self.assertRaises(PinConnectionError, Connection, self.pin3, self.pin4)

        # Connection from INPUT_PIN to OUTPUT_PIN is not valid
        self.assertRaises(PinConnectionError, Connection, self.pin4, self.pin1)

        # Connection from node with higher or equal level means circular reference
        self.assertRaises(PinConnectionError, Connection, self.pin2, self.pin3)

    def test_connection_correctlyAddedTheSameLevel_destinationNodeLevelIncreased(self):
        # Arrange
        node_zero = Node(3, 'tets', 'node_zero')
        node_zero.level = 0
        pin = Pin('pin', INPUT_PIN)
        pin.node = node_zero

        # Act
        connection = Connection(self.pin1, pin)

        # Assert
        self.assertEqual(node_zero.level, 1)
