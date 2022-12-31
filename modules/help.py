#!/bin/python3

def print_help():
    text = "\n"
    text += "COMMAND               DESCRIPTION\n"
    text += "=======               ===========\n"
    text += " help / ?             show this text\n"
    text += " sessions             get available machines\n"
    text += " whois <id>           get shell info\n"
    text += " connect <id>         connect to shell\n" 
    
    print(text)
