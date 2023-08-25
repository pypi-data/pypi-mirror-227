import pyappi
from colorama import Fore, Style
import httpx
import click
import json
import os

from pyappi.util.login import session_challenge

@click.command()
@click.argument('cmd')
@click.option("--id", default="", help="Id of resource to read")
@click.option("--proto", default="http", help="Protocol string, usually http or https")
@click.option("--host", default="127.0.0.1:8099", help="Host name or ip address with optional port after a :")
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
@click.option("--data", default="", help="Json string of data for the specified command")
def read(cmd, id, proto, host, user, password, data):
    result = httpx.get(f"{proto}://{host}/document/{id}?{session_challenge(user,password)}")
    print(cmd, id, result,result.status_code)


@click.command()
@click.argument('cmd')
@click.option("--id", default="", help="Id of resource to read")
@click.option("--proto", default="http", help="Protocol string, usually http or https")
@click.option("--host", default="127.0.0.1:8099", help="Host name or ip address with optional port after a :")
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
@click.option("--data", default="", help="Json string of data for the specified command")
def write(cmd, id, proto, host, user, password, data):
    write = json.parse(data)
    result = httpx.put(f"{proto}://{host}/document/{id}?{session_challenge(user,password)}", json=write)
    print(cmd, id, result,result.status_code)


@click.command()
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
def login(user, password):
    session = session_challenge(user, password)

    with open("appi_session.b64","w") as file:
        file.write(session)

@click.command()
def logout():
    try:
        os.remove("appi_session.b64")
    except Exception as _e:
        pass

@click.command()
@click.argument('cmd')
@click.option("--id", default="", help="Id of resource to read")
@click.option("--proto", default="http", help="Protocol string, usually http or https")
@click.option("--host", default="", help="Host name or ip address with optional port after a :")
@click.option("--user", default="", help="User name of account you are logging into.")
@click.option("--password", default="", help="Password of your account.")
@click.option("--data", default="", help="Json string of data for the specified command")
def main(cmd, id, proto, host, user, password):
    match cmd:
        case "read":
            return read()
        case "write":
            return write()
        case "login":
            return login()
        case "logout":
            return logout()
        case "about":
            print(f"{Fore.GREEN}PYAPPI-CLIENT {pyappi.__version__}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()