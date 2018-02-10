#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from databake.tests.integration_tests import common


def main():
    files_dir = 'input_files'
    for file_path in os.listdir(files_dir):
        common.get_graph(os.path.join(files_dir, file_path))


main()
