import pytest
from rich import print
from offline_conf_reader.test.fixtures import ehn1_daqconfig_sessions, variables_extracted
from offline_conf_reader.oks_data_extractor import OKSDataExtractor

def test_can_extract_data(ehn1_daqconfig_sessions, variables_extracted):
    for session_name, file_path in ehn1_daqconfig_sessions().items():
        print(f'Processing \'{session_name}\' in {file_path}')
        ode = OKSDataExtractor(oks_file_path=file_path, session_name=session_name)

        for variable_name, variable_type in variables_extracted.items():
            print(f'Checking variable \'{variable_name}\'')
            value = getattr(ode,variable_name)
            assert value is not None
            assert isinstance(value, variable_type)

def test_does_not_accept_include(ehn1_daqconfig_sessions, variables_extracted):
    for session_name, file_path in ehn1_daqconfig_sessions(False).items():
        print(f'Processing \'{session_name}\' in {file_path}')
        with pytest.raises(Exception):
            ode = OKSDataExtractor(oks_file_path=file_path, session_name=session_name)

