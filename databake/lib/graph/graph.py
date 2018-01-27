#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.graph.connection import Connection
from databake.lib.graph.exceptions import GraphError
from databake.lib.graph.node import Node
from databake.lib.graph.pin import Pin, OUTPUT_PIN, INPUT_PIN


class Graph:
    def __init__(self, recipe):
        self.recipe = recipe
        self.name = recipe.name
        self.nodes = {}
        self.connections = []

        for node in self.recipe.nodes:
            if self.nodes.get(node.id):
                msg = 'Graph can not contain two or more nodes with the same id'
                raise GraphError(msg)
            self.nodes[node.id] = Node(node.id, node.plugin, node.name)

        for connection in recipe.connections:
            from_pin = Pin(connection.from_pin.name, OUTPUT_PIN)
            from_node = self.nodes[connection.from_pin.node]
            from_node.add_pin(from_pin)
            to_pin = Pin(connection.to_pin.name, INPUT_PIN)
            to_node = self.nodes[connection.to_pin.node]
            to_node.add_pin(to_pin)
            tmp = Connection(from_pin, to_pin, connection.name)
            self.connections.append(tmp)





