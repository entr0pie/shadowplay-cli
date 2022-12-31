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

def read_session_info(dict_info) -> None:
    biggest_len = 0
    
    for key in dict_info:
        if len(key) > biggest_len:
            biggest_len = len(key)
    
    print()

    for key in dict_info:
        temp_key = key
        
        while len(temp_key) < biggest_len: 
            temp_key += " "

        print(f"{temp_key} | {dict_info[key]}")

    print()

def get_address_arg(command) -> tuple:
    _, addr = command.split(' ')
            
    try:
        ip, port = addr.split(':')
        port = int(port)

    except ValueError:
        sessions = open('sessions.tmp', 'r').readlines()
        index = int(addr)
        
        ip, port = sessions[index].strip().split(':')
        port = int(port)

    return (ip, port)
