#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from databake.lib.graph.exceptions import NodeError
from databake.lib.graph.node import Node
from databake.lib.graph.pin import INPUT_PIN, OUTPUT_PIN, Pin


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
        node = Node(self.node_id, self.plugin, self.name)
        pin = Pin('pin1', INPUT_PIN)

        # Act
        node.add_pin(pin)

        # Assert
        self.assertEqual(len(node.input_pins), 1)
        self.assertEqual(len(node.output_pins), 0)

    def test_addPin_addDuplicatedPin_noChangeInNode(self):
        # Arrange
        node = Node(self.node_id, self.plugin, self.name)
        pin = Pin('pin1', INPUT_PIN)

        # Act
        node.add_pin(pin)

        # Assert
        self.assertRaises(NodeError, node.add_pin, pin)
        self.assertEqual(len(node.input_pins), 1)
        self.assertEqual(len(node.output_pins), 0)

    def test_addPin_addMultipleOutputPins_correctlyAdded(self):
        # Arrange
        node = Node(self.node_id, self.plugin, self.name)

        # Act
        node.add_pin(Pin('pin1', INPUT_PIN))
        node.add_pin(Pin('pin2', INPUT_PIN))
        node.add_pin(Pin('pin3', OUTPUT_PIN))
        node.add_pin(Pin('pin4', OUTPUT_PIN))

        # Assert
        self.assertEqual(len(node.input_pins), 2)
        self.assertEqual(len(node.output_pins), 2)

    def test_addPin_pinIsNotPinType_raiseTypeError(self):
        # Arrange
        node = Node(self.node_id, self.plugin, self.name)

        # Assert
        self.assertRaises(TypeError, node.add_pin, 5)

    def test_removePin_removeExistingPin_correctlyRemoved(self):
        # Arrange
        node = Node(self.node_id, self.plugin, self.name)
        pin = Pin('pin1', INPUT_PIN)

        # Act
        node.add_pin(pin)
        node.remove_pin(pin)

        # Assert
        self.assertEqual(len(node.input_pins), 0)

    def test_removePin_removeNotExistingPin_PinNotInNodeErrorRaised(self):
        # Arrange
        node = Node(self.node_id, self.plugin, self.name)
        pin = Pin('pin1', INPUT_PIN)

        # Act / Assert
        self.assertRaises(NodeError, node.remove_pin, pin)
