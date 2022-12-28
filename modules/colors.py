#!/bin/python3

class Colors: 
    def __init__(self):
        self.ok = f"\u001b[32;1m"
        self.fail = f"\u001b[31;1m"
        self.warn = f"\u001b[33;1m"
        self.bold = f"\u001b[37;1m"
        self.reset = f"\u001b[0m"
