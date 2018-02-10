#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from databake.tests.integration_tests import common


def main():
    files_dir = 'input_files'
    for file_path in os.listdir(files_dir):
        print(f'=====> Testing {file_path} file:')
        graph = common.get_graph(os.path.join(files_dir, file_path))
        for node in graph.nodes.values():
            print(node.node_id, node.level)


main()
