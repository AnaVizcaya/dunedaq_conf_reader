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
    sessions = {}
    tempdir = tempfile.mkdtemp(prefix="ehn1-daqconfigs")
    repo = Repo.clone_from(cern_gitlab_url + ehn1_path, tempdir)
    root_dir = Path(tempdir)/"sessions"
    for session_file in os.listdir(root_dir):
        tree = parse(root_dir/session_file)
        print(f"\n\nProcessing file \'{session_file}\'")
        root = tree.getroot()

        oks_elements = root.findall("obj")
        for oks_element in oks_elements:
            if oks_element.attrib["class"] == "Session":
                session = oks_element.attrib["id"]
                print(f" - Session \'{session}\' found")
                sessions[session] = root_dir/session_file
    print('\n')
    return sessions


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