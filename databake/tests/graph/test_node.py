#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from databake.lib.graph.exceptions import InvalidPinTypeError
from databake.lib.graph.node import Node
from databake.lib.graph.pin import INPUT_PIN, OUTPUT_PIN


class TestNode(TestCase):
    def setUp(self):
        self.node_id = '1'
        self.plugin = 'core.example.plugin'
        self.name = 'ExampleName'

    def test_node_createEmptyObject_objectProperlyCreated(self):
        # Arrange
        # Act
        node = Node(self.node_id, self.plugin, self.name)

        # Assert
        self.assertIsInstance(node, Node)
        self.assertEqual(self.node_id, node.node_id)
        self.assertEqual(self.plugin, node.plugin)
        self.assertEqual(self.name, node.name)
        self.assertEqual(0, node.level)
        self.assertEqual([], node.input_pins)
        self.assertEqual([], node.output_pins)
        self.assertEqual({}, node.options)

    def test_addPin_addNewValidPin_pinCorrectlyAdded(self):
        # Arrange
        pin_name = 'pin1'
        pin_type = INPUT_PIN
        node = Node(self.node_id, self.plugin, self.name)

        # Act
        node.add_pin(pin_name, pin_type)

        # Assert
        self.assertEqual(len(node.input_pins), 1)
        self.assertEqual(len(node.output_pins), 0)

    def test_addPin_addPinWithNoValidType_raiseException(self):
        # Arrange
        pin_name = 'pin1'
        pin_type = 'not_valid'
        node = Node(self.node_id, self.plugin, self.name)

        # Act/Assert
        self.assertRaises(InvalidPinTypeError, node.add_pin, pin_name, pin_type)

    def test_addPin_addDuplicatedPin_noChangeInNode(self):
        # Arrange
        pin_name = 'pin1'
        pin_type = INPUT_PIN
        node = Node(self.node_id, self.plugin, self.name)

        # Act
        node.add_pin(pin_name, pin_type)
        node.add_pin(pin_name, pin_type)

        # Assert
        self.assertEqual(len(node.input_pins), 1)
        self.assertEqual(len(node.output_pins), 0)

    def test_addPin_addMultipleOutputPins_correctlyAdded(self):
        # Arrange
        node = Node(self.node_id, self.plugin, self.name)

        # Act
        node.add_pin('pin1', INPUT_PIN)
        node.add_pin('pin2', INPUT_PIN)
        node.add_pin('pin3', OUTPUT_PIN)
        node.add_pin('pin4', OUTPUT_PIN)

        # Assert
        self.assertEqual(len(node.input_pins), 2)
        self.assertEqual(len(node.output_pins), 2)
