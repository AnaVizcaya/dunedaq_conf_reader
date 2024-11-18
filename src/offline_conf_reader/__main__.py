import click
from  offline_conf_reader.oks_data_extractor import OKSDataExtractor


def list_variable_callback(dummy0, dummy1, dummy2):
    ode = OKSDataExtractor("dummy", "dummy")
    for v in ode.get_variables():
        print(f'{v.name}: {v.type}')
    exit(0)

@click.command("offline-conf-reader")
@click.option("--list-variables", callback=list_variable_callback, is_flag=True)
@click.argument("config_file", type=click.Path(exists=True))
@click.argument('session_name', type=str)
@click.argument("variable_name", type=str, nargs=-1)
def main(config_file:str, session_name:str, variable_name:list[str], list_variables:bool):

    if list_variables:
        return

    ode = OKSDataExtractor(config_file, session_name)
    for var in variable_name:
        value = getattr(ode, var)
        if value is None:
            print(f"ERROR: Variable {var} not found")
