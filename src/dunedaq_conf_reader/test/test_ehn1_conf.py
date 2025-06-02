import pytest
from dunedaq_conf_reader.test.fixtures import ehn1_daqconfig_file_and_sessions, variables_extracted
from dunedaq_conf_reader.dunedaq_conf_data_extractor import DUNEDAQConfDataExtractor
from rich import print
import os


def test_ehn1_daqconfig_sessions(ehn1_daqconfig_file_and_sessions, variables_extracted, branch_name, repository):
    assert ehn1_daqconfig_file_and_sessions is not None
    assert variables_extracted is not None

    for json_file, session_names in ehn1_daqconfig_file_and_sessions.items():
        for session_name in session_names:
            print(f"Processing session \'{session_name}\'")
            print(f" - Session path: \'{json_file}\'")
            ddcde = DUNEDAQConfDataExtractor(json_file, session_name)
            for var in variables_extracted.keys():
                value = getattr(ddcde, var, None)
                if value is None:
                    basename = os.path.basename(json_file).replace(".json", ".xml")
                    print(f" - \'{var}\' could not be extracted from the branch \'{branch_name}\' in the repo \'{repository}\', session: \'{session_name}\' in file \'sessions/{basename}\'.")
                else:
                    print(f" - \'{var}\': {value}")

                assert value is not None