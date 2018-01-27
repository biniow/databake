#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from mock import mock

from databake.lib.graph.exceptions import NodeError
from databake.lib.graph.node import Node
from databake.lib.graph.pin import INPUT_PIN, OUTPUT_PIN, Pin


class TestNode(TestCase):
    def setUp(self):
        self.node_id = '1'
        self.plugin = 'databake.tests.plugins.join_test'
        self.name = 'ExampleName'

        self.plugin1_mock = mock.MagicMock(
            __version__='1.0.0',
            __author__='Wojciech Biniek',
            __email__='wojtek.biniek@gmail.com',
            __plugin_name__='Join plugin',
            __input_pins__=['left_df', 'right_df'],
            __output_pins__=['output'],
            __parameters__={
                'join_type': str
            }
        )

    def test_node_createEmptyObject_objectProperlyCreated(self):
        # Arrange
        # Act
        node = Node(self.node_id, self.plugin, self.name, auto_import=False)

        # Assert
        self.assertIsInstance(node, Node)
        self.assertEqual(self.node_id, node.node_id)
        self.assertEqual(self.plugin, node.plugin_name)
        self.assertEqual(self.name, node.name)
        self.assertEqual(0, node.level)
        self.assertEqual([], node.input_pins)
        self.assertEqual([], node.output_pins)
        self.assertEqual({}, node.parameters)

    def test_addPin_addNewValidPin_pinCorrectlyAdded(self):
        # Arrange
        node = Node(self.node_id, self.plugin, self.name, auto_import=False)
        pin = Pin('pin1', INPUT_PIN)

        # Act
        node.add_pin(pin)

        # Assert
        self.assertEqual(len(node.input_pins), 1)
        self.assertEqual(len(node.output_pins), 0)

    def test_addPin_addDuplicatedPin_noChangeInNode(self):
        # Arrange
        node = Node(self.node_id, self.plugin, self.name, auto_import=False)
        pin = Pin('pin1', INPUT_PIN)

        # Act
        node.add_pin(pin)

        # Assert
        self.assertRaises(NodeError, node.add_pin, pin)
        self.assertEqual(len(node.input_pins), 1)
        self.assertEqual(len(node.output_pins), 0)

    def test_addPin_addMultipleOutputPins_correctlyAdded(self):
        # Arrange
        node = Node(self.node_id, self.plugin, self.name, auto_import=False)

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
        node = Node(self.node_id, self.plugin, self.name, auto_import=False)
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

    @mock.patch('importlib.import_module')
    def test_importConfigFromPlugin_normalExecution_validNumberOfPinsAssociated(self, importlib):
        # Arrange
        importlib.return_value = self.plugin1_mock
        node = Node(1, 'plugin_name', 'Node', auto_import=False)

        # Act
        node.import_config_from_plugin()

        # Assert
        self.assertEqual(len(node.input_pins), 2)
        self.assertEqual(len(node.output_pins), 1)


