#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.graph.connection import Connection
from databake.lib.graph.exceptions import GraphError
from databake.lib.graph.node import Node


class Graph:
    def __init__(self, recipe, auto_init=True):
        self.recipe = recipe
        self.name = recipe.graph_name
        self.nodes = {}
        self.connections = []

        if auto_init:
            self.init_nodes()
            self.init_connections()

    def init_nodes(self):
        for node in self.recipe.nodes:
            if self.nodes.get(node.id):
                msg = f'Graph can not contain two or more nodes with the same id: {node.id}'
                raise GraphError(msg)
            self.nodes[node.id] = Node(node.id, node.plugin_name, node.name, node.parameters)

    def init_connections(self):
        for connection in self.recipe.connections:
            try:
                from_pin = self.nodes[connection.from_pin.node].get_pin_by_name(connection.from_pin.pin)
                to_pin = self.nodes[connection.to_pin.node].get_pin_by_name(connection.to_pin.pin)
            except KeyError:
                if not self.nodes:
                    raise GraphError('Nodes list is empty. Have you initialized nodes?')
                raise
            tmp = Connection(from_pin, to_pin, connection.name)
            self.connections.append(tmp)

