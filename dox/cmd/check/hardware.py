import click
import psutil
import platform
from socket import socket, AF_INET, SOCK_DGRAM
import requests
import re
from tabulate import tabulate


def _get_public_ip():
    try:
        req = requests.get("http://ipconfig.kr")
        return re.search(r"IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", req.text)[1]
    except requests.exceptions.RequestException:
        return "Unable"


@click.command()
def hardware():
    # CPU Information
    cpu_cores_physical = psutil.cpu_count(logical=False)

    # Memory Information
    mem = psutil.virtual_memory()
    total_memory = mem.total
    available_memory = mem.available

    # Disk Information (Disk Size)
    disks = psutil.disk_partitions()
    disk_sizes = [(disk.device, disk.mountpoint, psutil.disk_usage(disk.mountpoint).total) for disk in disks]
    disk_sizes.sort(key=lambda x: x[2], reverse=True)
    disk_table = [
        ["", device, mount_point, f"{size // (1024 ** 3)} GB"] for device, mount_point, size in disk_sizes[:5]
    ]

    # Network IPs (Assuming IPv4)
    sock = socket(AF_INET, SOCK_DGRAM)
    try:
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
    click.echo(f"Memory:     {available_memory // (1024 ** 3)} / {total_memory // (1024 ** 3)} GB")
    click.echo("Disk Size:")
    click.echo(tabulate(disk_table, tablefmt="plain"))
    click.echo(f"Local IP:   {local_ip}")
    click.echo(f"Public IP:  {public_ip}")


if __name__ == "__main__":
    hardware()

    disk_table = []
    for i in range(min(len(disk_sizes), 5)):
        device, mount_point, size = disk_sizes[i]
        disk_table.append(["  ", device, mount_point, f"{toGB(size):.0f} GB"])

    click.echo(tabulate(disk_table, tablefmt="plain"))

    click.echo(f"Local IP:   {local_ip}")
    click.echo(f"Public IP:  {public_ip}")


if __name__ == "__main__":
    hardware()
