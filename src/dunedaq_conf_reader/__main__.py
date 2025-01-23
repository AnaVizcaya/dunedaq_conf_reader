import click
from  dunedaq_conf_reader.dunedaq_conf_data_extractor import DUNEDAQConfDataExtractor
import logging
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler()])


def list_variable_callback(ctx, param, value):
    if value:
        ode = DUNEDAQConfDataExtractor()
        for v in ode.get_variables():
            print(f'{v.name}: {v.type}')
        exit(0)

@click.command("dunedaq-conf-reader")
@click.option("-l", "--list-variables", callback=list_variable_callback, is_flag=True)
@click.argument("config_file", type=click.Path(exists=True))
@click.argument('session_name', type=str)
@click.argument("variable_name", type=str, nargs=-1)
def main(config_file:str, session_name:str, variable_name:list[str], list_variables:bool):

    if list_variables:
        return

    ode = DUNEDAQConfDataExtractor(config_file, session_name)
    for var in variable_name:
        value = getattr(ode, var)

        if value is None:
            print(f"ERROR: Variable {var} not found")

        if type(value) is dict:
            for k, v in value.items():
                if isinstance(k, tuple):
                    print(f'{k[0]} FEMB{k[1]}: {v}')
                else:
                    print(f'{k}: {v}')

        else:
            print(value)