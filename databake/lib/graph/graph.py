#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.graph.connection import Connection
from databake.lib.graph.exceptions import GraphError
from databake.lib.graph.node import Node
from databake.lib.graph.pin import Pin, OUTPUT_PIN, INPUT_PIN


class Graph:
    def __init__(self, recipe, auto_init=True):
        self.recipe = recipe
        self.name = recipe.name
        self.nodes = {}
        self.connections = []

        if auto_init:
            self.init_nodes()
            self.init_connections()

    def init_nodes(self):
        for node in self.recipe.nodes:
            if self.nodes.get(node.id):
                msg = 'Graph can not contain two or more nodes with the same id'
                raise GraphError(msg)
            self.nodes[node.id] = Node(node.id, node.plugin_name, node.name)

    def init_connections(self):
        for connection in self.recipe.connections:
            try:
                from_pin = self.nodes[connection.from_pin.node].get_pin_by_name(connection.from_pin.name)
                to_pin = self.nodes[connection.to_pin.node].get_pin_by_name(connection.to_pin.name)
            except KeyError:
                if not self.nodes:
                    raise GraphError('Nodes list is empty. Have you initialized nodes?')
                raise
            tmp = Connection(from_pin, to_pin, connection.name)
            self.connections.append(tmp)





