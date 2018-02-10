#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
from unittest import TestCase

import mock

from databake.lib.graph.connection import Connection
from databake.lib.graph.exceptions import GraphError
from databake.lib.graph.graph import Graph
from databake.lib.graph.node import Node


class TestGraph(TestCase):
    def setUp(self):
        self.node1 = mock.MagicMock()
        self.node1.id = 1
        self.node1.plugin_name = 'databake.tests.plugins_mocks.join_test'
        self.node1.name = 'join_first'
        self.node1.parameters = {'join_type': 'left'}
        self.node1.import_config_from_plugin = mock.MagicMock()

        self.node2 = mock.MagicMock()
        self.node2.id = 2
        self.node2.plugin_name = 'databake.tests.plugins_mocks.where_test'
        self.node2.name = 'filtering results'
        self.node2.parameters = {'condition': 'a > 10'}
        self.node2.import_config_from_plugin = mock.MagicMock()

        self.connection1 = mock.MagicMock()
        self.connection1.name = 'node1 to node2'
        self.connection1.from_pin = mock.MagicMock()
        node1_plugin = importlib.import_module(self.node1.plugin_name)
        self.connection1.from_pin.pin = node1_plugin.__output_pins__[0]
        self.connection1.from_pin.node = 1

        self.connection1.to_pin = mock.MagicMock()
        node2_plugin = importlib.import_module(self.node2.plugin_name)
        self.connection1.to_pin.pin = node2_plugin.__input_pins__[0]
        self.connection1.to_pin.node = 2

    def test_graph_setGraphNameFromRecipe_setCorrectly(self):
        # Arrange
        valid_value = 'test_name'
        recipe = mock.MagicMock()
        recipe.graph_name = valid_value

        # Act
        graph = Graph(recipe)

        # Assert
        self.assertEqual(graph.name, valid_value)

    def test_initNodes_setNodesFromRecipe_nodesDictValidLength(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]

        # Act
        graph = Graph(recipe, auto_init=False)
        graph.init_nodes()

        # Assert
        self.assertEqual(len(graph.nodes), 2)

    def test_initNodes_setNodesFromRecipe_nodesDictValidKeys(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]

        # Act
        graph = Graph(recipe, auto_init=False)
        graph.init_nodes()

        # Assert
        valid_keys = [1, 2]
        self.assertEqual(sorted(graph.nodes.keys()), valid_keys)

    def test_initNodes_setNodesFromRecipe_nodeClassObjectsInside(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]

        # Act
        graph = Graph(recipe, auto_init=False)
        graph.init_nodes()

        # Assert
        self.assertIsInstance(graph.nodes[1], Node)

    def test_graph_recipeWithDuplicatedNodes_raiseGraphError(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node1]
        graph = Graph(recipe, auto_init=False)

        # Act/Assert
        self.assertRaises(GraphError, graph.init_nodes)

    def test_initConnections_setConnectionsFromRecipe_connectionsListValidLenght(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]
        recipe.connections = [self.connection1]

        # Act
        graph = Graph(recipe, auto_init=False)
        graph.init_nodes()
        graph.init_connections()

        # Assert
        self.assertEqual(len(graph.connections), 1)

    def test_initConnections_setConnectionFromRecipe_connectionClassObjectInside(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]
        recipe.connections = [self.connection1]

        # Act
        graph = Graph(recipe, auto_init=False)
        graph.init_nodes()
        graph.init_connections()

        # Assert
        self.assertIsInstance(graph.connections[0], Connection)

    def test_initConnections_notInitializedNodesBefore_raisedGraphError(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]
        recipe.connections = [self.connection1]
        graph = Graph(recipe, auto_init=False)

        # Act / Assert
        self.assertRaises(GraphError, graph.init_connections)

    def test_initConnections_nodeOrPinNotFound_raiseKeyError(self):
        # Arrange
        node = mock.MagicMock()
        node.id = 3
        node.plugin_name = 'databake.tests.plugins_mocks.join_test'
        node.name = 'join_first'
        node.parameters = {'join_type': 'left'}
        node.import_config_from_plugin = mock.MagicMock()

        recipe = mock.MagicMock()
        plugin_name = 'databake.tests.plugins_mocks.join_test'
        recipe.nodes = [self.node1, node]
        recipe.connections = [self.connection1]
        graph = Graph(recipe, auto_init=False)
        graph.init_nodes()

        # Act / Assert
        self.assertRaises(KeyError, graph.init_connections)
