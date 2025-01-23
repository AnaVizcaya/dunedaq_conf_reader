import pytest
from git import Repo
import json
import tempfile
import os
from pathlib import Path
from rich import print
from daqconf.jsonify import jsonify_xml_data


@pytest.fixture
def ehn1_daqconfig_file_and_sessions(branch_name, repository):
    files_sessions = {}

    tempdir = tempfile.mkdtemp(prefix="ehn1-daqconfigs")
    repo = Repo.clone_from(repository, tempdir, branch=branch_name)

    repo_directories = [x for x in os.listdir(tempdir) if os.path.isdir(Path(tempdir)/x)]

    root_dir = Path(tempdir) / "sessions"

    for session_file in os.listdir(root_dir):

        print(f"\nJsonifying DB \'{session_file}\'")
        os.environ["DUNEDAQ_DB_PATH"] = os.environ["DUNEDAQ_DB_PATH"] + ":".join(repo_directories)
        xml_file = str(root_dir/session_file)
        json_file = xml_file.replace(".xml", ".json")
        jsonify_xml_data(xml_file, json_file)

        print(f"Processing file \'{json_file}\'")
        with open(json_file, "r") as f:
            data = json.load(f)

            for key, value in data.items():
                if key.endswith("@Session"):
                    session_name = key.replace("@Session", "")
                    print(f" - Session \'{session_name}\' found")
                    if json_file not in files_sessions:
                        files_sessions[json_file] = []
                    files_sessions[json_file].append(session_name)

    print('\n')
    return files_sessions


@pytest.fixture
def variables_extracted():
    return {
        # WIB settings
        "adc_test_pattern" : dict[str,bool],
        "cold"             : dict[str,bool],
        "detector_type"    : dict[str,int ],
        "pulser"           : dict[str,bool],
        "pulse_dac"        : dict[str,int ],

        # FEMB settings
        "ac_couple"        : dict[str,bool],
        "baseline"         : dict[str,int ],
        "buffering"        : dict[str,int ],
        "enabled"          : dict[str,bool],
        "gain"             : dict[str,int ],
        "gain_match"       : dict[str,bool],
        "leak"             : dict[str,int ],
        "leak_10x"         : dict[str,bool],
        "leak_f"           : dict[str,float], # calculated from the above 2
        "peak_time"        : dict[str,int ],
        "strobe_delay"     : dict[str,int ],
        "strobe_length"    : dict[str,int ],
        "strobe_skip"      : dict[str,int ],
        "test_cap"         : dict[str,bool],
    }


@pytest.fixture
def test_config_root():
    path = Path(__file__)
    config = path.parent / "test-config.data.json"
    config = os.path.abspath(config)
    with open(config, "r") as f:
        data = json.load(f)
        return data
