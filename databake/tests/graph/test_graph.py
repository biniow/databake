#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        self.node1.plugin = 'plugins.core.join'
        self.node1.name = 'join_first'

        self.node2 = mock.MagicMock()
        self.node2.id = 2
        self.node2.plugin = 'plugins.core.where'
        self.node2.name = 'filtering results'

        self.connection1 = mock.MagicMock()
        self.connection1.name = 'node1 to node2'
        self.connection1.from_pin = mock.MagicMock()
        self.connection1.from_pin.name = 'pin1'
        self.connection1.from_pin.node = 1
        self.connection1.to_pin = mock.MagicMock()
        self.connection1.to_pin.name = 'pin2'
        self.connection1.to_pin.node = 2

    def test_graph_setGraphNameFromRecipe_setCorrectly(self):
        # Arrange
        valid_value = 'test_name'
        recipe = mock.MagicMock()
        recipe.name = valid_value

        # Act
        graph = Graph(recipe)

        # Assert
        self.assertEqual(graph.name, valid_value)

    def test_graph_setNodesFromRecipe_nodesDictValidLength(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]

        # Act
        result = Graph(recipe).nodes

        # Assert
        self.assertEqual(len(result), 2)

    def test_graph_setNodesFromRecipe_nodesDictValidKeys(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]

        # Act
        result = Graph(recipe).nodes

        # Assert
        valid_keys = [1, 2]
        self.assertEqual(sorted(result.keys()), valid_keys)

    def test_graph_setNodesFromRecipe_nodeClassObjectsInside(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]

        # Act
        result = Graph(recipe).nodes

        # Assert
        self.assertIsInstance(result[1], Node)

    def test_graph_recipeWithDuplicatedNodes_raiseGraphError(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node1]

        # Act/Assert
        self.assertRaises(GraphError, Graph, recipe)

    def test_graph_setConnectionsFromRecipe_connectionsListValidLenght(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]
        recipe.connections = [self.connection1]

        # Act
        result = Graph(recipe).connections

        # Assert
        self.assertEqual(len(result), 1)

    def test_graph_setConnectionFromRecipe_connectionClassObjectInside(self):
        # Arrange
        recipe = mock.MagicMock()
        recipe.nodes = [self.node1, self.node2]
        recipe.connections = [self.connection1]

        # Act
        result = Graph(recipe).connections

        # Assert
        self.assertIsInstance(result[0], Connection)

