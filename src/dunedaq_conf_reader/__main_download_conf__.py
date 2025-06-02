import click
import os
import json
import requests
from rich import print
from rich.table import Table
from rich.prompt import Confirm
import tarfile
import shutil


def get_dot_drunc_json():
    """Read the ~/.drunc.json file"""
    data = {}
    with open(os.path.expanduser("~/.drunc.json"), "r") as f:
        data = json.load(f)["run_registry_configuration"]
    assert data.get("socket") is not None, "socket is not set in the ~/.drunc.json file"
    assert data.get("user") is not None, "user is not set in the ~/.drunc.json file"
    assert data.get("password") is not None, "password is not set in the ~/.drunc.json file"
    return data


def get_last_conf_number(n_run: int):
    """Get the last configuration number for a given run number"""
    dot_drunc_json = get_dot_drunc_json()
    response = requests.get(
        f"{dot_drunc_json['socket']}/runregistry/getRunMetaLast/{n_run}",
        auth=(dot_drunc_json["user"], dot_drunc_json["password"])
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        exit(1)

    return response.json()

def _download_run_conf(run_number: int):
    """Download the configuration for a given run number"""
    dot_drunc_json = get_dot_drunc_json()


    response = requests.get(
        f"{dot_drunc_json['socket']}/runregistry/getRunMeta/{run_number}",
        auth=(dot_drunc_json["user"], dot_drunc_json["password"]),
    )

    try:
        response.raise_for_status()
        data = response.json()
        if "Exception" in data:
            raise Exception(f"Service response: {data['Exception']}")

    except requests.exceptions.HTTPError as e:
        print(e)
        exit(1)

    except Exception as e:
        print(e)
        print(f"Run {run_number} does not have metadata aborting...")
        exit(1)

    response = requests.get(
        f"{dot_drunc_json['socket']}/runregistry/getRunBlob/{run_number}",
        auth=(dot_drunc_json["user"], dot_drunc_json["password"]),
    )
    try:
        response.raise_for_status()
    except Exception as e:
        print(e)
        print(f"Run {run_number} not found, aborting...")
        exit(1)


    with open(f"run_{run_number}.tar.gz", "wb") as f:
        f.write(response.content)

    directory = f"run_{run_number}"

    if os.path.exists(directory):
        answer = Confirm.ask(f"{directory} directory already exists, do you want to remove it?", default=False)
        if answer:
            shutil.rmtree(directory)
        else:
            os.remove(f"run_{run_number}.tar.gz")
            print("Aborting...")
            exit(1)

    os.makedirs(directory, exist_ok=True)

    with tarfile.open(f"./run_{run_number}.tar.gz", "r:gz") as tar:
        tar.extractall(directory)

    entry_point_file = None#f"{directory}/*entry_point.txt"
    entry_point = None
    json_conf_file = None

    for file in os.listdir(directory):
        if file.endswith(".data.json"):
            json_conf_file = file
        elif file.endswith("_entry_point.txt"):
            entry_point_file = file

    entry_point_file = os.path.join(directory, entry_point_file)
    json_conf_file = os.path.join(directory, json_conf_file)

    if entry_point_file is None:
        print(f"{directory}/tmp*_entry_point.txt file not found, aborting...")
        exit(1)

    if json_conf_file is None:
        print(f"{directory}/tmp*.data.json file not found, aborting...")
        exit(1)

    with open(entry_point_file, "r") as f:
        entry_point = f.read()

    print(f"""Configuration for run {run_number} downloaded in [green]{directory}[/green], to show the configuration, use:
[yellow]dunedaq-conf-reader {json_conf_file} {entry_point}[/yellow]""")



@click.group()
def main():
    pass

@main.command("show-last-n-run-metadata")
@click.argument("number", type=int)
def show_last_n_run_metadata(number: int):
    """Show the metadata for the last n runs"""
    print(f"Displaying the metadata for the last {number} runs")
    data = get_last_conf_number(number)
    table = Table(title="Run Metadata")
    table.add_column("Run Number", style="cyan")
    table.add_column("Start time", style="magenta")
    table.add_column("Stop time", style="green")
    table.add_column("Detector ID", style="blue")
    table.add_column("Run type", style="red")
    table.add_column("Software version", style="yellow")
    for run in data[1]:
        table.add_row(str(run[0]), str(run[1]), str(run[2]), str(run[3]), str(run[4]), str(run[5]))
    print(table)


@main.command("download-last-n-run-conf")
@click.argument("number", type=int)
def download_last_n_run_conf(number: int):
    """Download the last configuration for a given name"""
    print(f"Downloading the last {number} run configurations")
    data = get_last_conf_number(number)
    for run in data[1]:
        print(f"Downloading configuration for run {run[0]}")
        _download_run_conf(run[0])


@main.command("download-run-conf")
@click.argument("run_number", type=int)
def download_run_conf(run_number: int):
    """Download the configuration for a given run number"""
    print(f"Downloading configuration for run {run_number}")
    _download_run_conf(run_number)


if __name__ == "__main__":
    main()