#!/bin/python3

def read_session_file():
    file = open('sessions.tmp', 'r').readlines()
    text =  "\n"
    text += "SESSIONS\n"
    text += "========\n\n"
    
    text += " ID         | ADDRESS\n"
    text += " -----------------------------------\n"
    
    for i in range(len(file)):
        file[i] = file[i].strip()
        address, port = file[i].split(":")
        text += f" {i}          | {address}:{port}\n"

    print(text)


