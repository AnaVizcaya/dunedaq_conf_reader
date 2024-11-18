import pytest
from git import Repo
import tempfile
import os
from pathlib import Path
from defusedxml.ElementTree import parse
from rich import print

cern_gitlab_url = "ssh://git@gitlab.cern.ch:7999"
repo_name = "ehn1-daqconfigs"
ehn1_path = f"/dune-daq/online/{repo_name}.git"


@pytest.fixture
def ehn1_daqconfig_sessions():
    def _ehn1_daqconfig_sessions(consolidate_conf=True):
        sessions = {}
        tempdir = tempfile.mkdtemp(prefix="ehn1-daqconfigs")
        repo = Repo.clone_from(cern_gitlab_url + ehn1_path, tempdir)

        repo_directories = [x for x in os.listdir(tempdir) if os.path.isdir(Path(tempdir)/x)]

        root_dir = Path(tempdir)/"sessions"

        for session_file in os.listdir(root_dir):

            if consolidate_conf:
                print(f"\nConsolidating DB \'{session_file}\'")
                os.environ["DUNEDAQ_DB_PATH"] = os.environ["DUNEDAQ_DB_PATH"] + ":".join(repo_directories)
                from daqconf.consolidate import consolidate_db
                consolidate_db(str(root_dir/session_file), str(root_dir/f"consolidated_{session_file}"))
                session_file = root_dir/f"consolidated_{session_file}"
            else:
                session_file = root_dir/session_file

            tree = parse(session_file)
            print(f"\nProcessing file \'{session_file}\'")
            root = tree.getroot()

            oks_elements = root.findall("obj")
            for oks_element in oks_elements:
                if oks_element.attrib["class"] == "Session":
                    session = oks_element.attrib["id"]
                    print(f" - Session \'{session}\' found")
                    sessions[session] = root_dir/session_file
        print('\n')
        return sessions
    return _ehn1_daqconfig_sessions


@pytest.fixture
def variables_extracted():
    return {
        "buffer": object,
        "ac_couple": object,
        "pulse_dac": object,
        "pulser": object,
        "baseline": object,
        "gain": object,
        "leak": object,
        "leak_10x": object,
        "peak_time": object,
        "enable_femb_fake_data": object,
        "test_cap": object,
        "APAs": list[int],
        "FEMBs": list[int],
        "pulse_period": object,
        "phase_group": object,
        "phases": object,
    }


@pytest.fixture
def test_config():
    path = Path(__file__)
    config = path.parent / "test-config.data.xml"
    config = os.path.abspath(config)
    return config