#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Connection:
    def __init__(self, from_pin, to_pin, comment=None):
        self.from_pin = from_pin
        self.to_pin = to_pin
        self.comment = comment
