import click
import psutil
from dox.utils.helpers import *

import platform
from socket import socket, AF_INET, SOCK_DGRAM
import requests
import re


def _get_public_ip():
    try:
        req = requests.get("http://ipconfig.kr")
        return re.search(r"IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", req.text)[1]

    except requests.exceptions.RequestException as e:
        return "Unable"


@click.command()
def hardware():
    """TODO: Check hardware configuration."""
    # CPU Information
    cpu_cores_physical = psutil.cpu_count(logical=False)
    cpu_cores_logical = psutil.cpu_count(logical=True)

    # Memory Information
    mem = psutil.virtual_memory()
    total_memory = mem.total
    available_memory = mem.available

    # Disk Information (Disk Size)
    disk = psutil.disk_usage("/")  # TODO: 환경변수로 특정 mountmoint를 지정할 수 있도록
    available_disk_size = disk.free
    total_disk_size = disk.total

    # Network IPs (Assuming IPv4)
    sock = socket(AF_INET, SOCK_DGRAM)
    try:
        # This doesn't actually connect but gets the routing info
        sock.connect(("8.8.8.8", 1))
        local_ip = sock.getsockname()[0]
    except Exception:
        local_ip = "N/A"
    finally:
        sock.close()

    # Public IP
    public_ip = _get_public_ip()

    # OS Information
    os_name = platform.system()
    os_version = platform.release()

    # Printing Extracted Information
    click.echo(f"OS Name:    {os_name}")
    click.echo(f"OS Version: {os_version}")
    click.echo(f"CPU Cores:  {cpu_cores_physical}")
    click.echo(f"Memory:     {toGB(available_memory):<4.0f} / {toGB(total_memory):<4.0f} GB")
    click.echo(f"Disk Size:  {toGB(available_disk_size):<4.0f} / {toGB(total_disk_size):<4.0f} GB")
    click.echo(f"Local IP:   {local_ip}")
    click.echo(f"Public IP:  {public_ip}")


if __name__ == "__main__":
    hardware()
