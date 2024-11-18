import pytest
from rich import print
from offline_conf_reader.test.fixtures import ehn1_daqconfig_sessions, variables_extracted
from offline_conf_reader.oks_data_extractor import OKSDataExtractor

def test_can_extract_wib_buffer(ehn1_daqconfig_sessions, variables_extracted):
    for session_name, file_path in ehn1_daqconfig_sessions.items():
        print(f'Processing \'{session_name}\' in {file_path}')
        ode = OKSDataExtractor(session_name, oks_file_path=file_path)

        for variable_name, variable_type in variables_extracted.items():
            print(f'Checking variable \'{variable_name}\'')
            value = getattr(ode,variable_name)
            assert value is not None
            assert isinstance(value, variable_type)

