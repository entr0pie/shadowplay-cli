# shadowplay-cli
Client for Shadowplay Command-and-Control (C&amp;C) server. Master your shells. 

<img src="images/shadowplay-cli.png">

## How does it work? 
The client (shadowplay-cli.py) connect to an node (server running shadowplay-srv.py), which have shells connected on it. Then, the user can control any of the shells available on the server, including more than one in the same session.

## Installation

```
git clone https://github.com/entr0pie/shadowplay-cli
```

## Basic Usage

Starting the program:

```
python3 shadowplay-cli.py --node <user>@<ip>:port
```

After authenticated, the first thing to do is getting the available shells.

```
$ sessions
```

To connect into any shell, type:

```
$ connect <ip>:<port>
```

## How can I contribute to the project? 

These topics are under development: 

- [X] Create basic connections and protocols srv-cli.
- [X] Implementing MD5 and TOKEN session methods.
- [ ] Error handling on connections and methods. 

- [ ] Handling more than one session per time.
- [ ] Use end-to-end cryptography on cli-srv communications.
- [ ] GET INFO function on the cli (get server and shell's basic information)

## License
This project is under [GNU GPLv3.](LICENSE)