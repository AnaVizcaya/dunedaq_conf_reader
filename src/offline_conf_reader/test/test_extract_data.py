import pytest
from rich import print
from offline_conf_reader.test.fixtures import ehn1_daqconfig_sessions, variables_extracted, test_config
from offline_conf_reader.oks_data_extractor import OKSDataExtractor
from offline_conf_reader.oks_utils import find_session, get_one, get_many
import os
from pathlib import Path
from defusedxml.ElementTree import parse


def test_find_session(test_config):
    tree = parse(test_config)
    session_name = 'test-config'
    root = tree.getroot()
    session = find_session(root, session_name)
    assert session is not None
    assert session.attrib['id'] == session_name


def test_get_one_relationship_by_class(test_config):
    tree = parse(test_config)
    session_name = 'test-config'
    root = tree.getroot()
    session = find_session(root, session_name)
    assert get_one(root, session, class_name="OpMonURI")


def test_get_one_relationship_by_name(test_config):
    tree = parse(test_config)
    session_name = 'test-config'
    root = tree.getroot()
    session = find_session(root, session_name)
    assert get_one(root, session, object_name="opmon_uri")


def test_get_one_attribute_by_name(test_config):
    tree = parse(test_config)
    session_name = 'test-config'
    root = tree.getroot()
    session = find_session(root, session_name)
    assert get_one(root, session, object_name="controller_log_level")


def test_get_many_by_class(test_config):
    tree = parse(test_config)
    session_name = 'test-config'
    root = tree.getroot()
    session = find_session(root, session_name)
    root_segment = get_one(root, session, object_name="segment")
    assert len(get_many(root, root_segment, class_name="Segment")) == 4


def test_get_many_by_name(test_config):
    tree = parse(test_config)
    session_name = 'test-config'
    root = tree.getroot()
    session = find_session(root, session_name)
    root_segment = get_one(root, session, object_name="segment")
    assert len(get_many(root, root_segment, obj_name="segments")) == 4


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