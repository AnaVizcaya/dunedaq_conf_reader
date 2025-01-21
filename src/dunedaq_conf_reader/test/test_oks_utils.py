import pytest
from dunedaq_conf_reader.test.fixtures import test_config_root, ehn1_daqconfig_sessions
from dunedaq_conf_reader.oks_utils import (
    OKSValueError,
    find_session,
    get_one_object,
    get_many_object,
    get_one_relation_by_class,
    get_one_relation_by_name,
    get_many_relation_by_class,
    get_many_relation_by_name,
    get_one_attribute,
    check_for_data_includes,
    get,
)
from defusedxml.ElementTree import parse


def test_get_one_object_by_object_id(test_config_root):
    session = get_one_object(test_config_root, object_id="test-config")
    assert session is not None
    assert session.attrib['id'] == "test-config"
    assert session.attrib['class'] == "Session"

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, object_id="duplicate-test-config")

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, object_id="non-existing-test-config")


def test_get_one_object_by_class_name(test_config_root):
    avx = get_one_object(test_config_root, class_name="AVXAbsRunSumProcessor")
    assert avx is not None
    assert avx.attrib['id'] == "tpg-absrs-proc"
    assert avx.attrib['class'] == "AVXAbsRunSumProcessor"

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, class_name="Session")

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, class_name="NotASession")


def test_get_one_object_by_object_id_and_class_name(test_config_root):
    avx = get_one_object(test_config_root, class_name="AVXAbsRunSumProcessor", object_id="tpg-absrs-proc")
    assert avx is not None
    assert avx.attrib['id'] == "tpg-absrs-proc"
    assert avx.attrib['class'] == "AVXAbsRunSumProcessor"

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, class_name="Session", object_id="bananas")

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, class_name="Bananas", object_id="tpg-absrs-proc")

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, class_name="Session", object_id="duplicate-test-config")


def test_find_session(test_config_root):
    session = find_session(test_config_root, 'test-config')
    assert session is not None
    assert session.attrib['id'] == 'test-config'
    assert session.attrib['class'] == 'Session'

    with pytest.raises(OKSValueError):
        find_session(test_config_root, 'duplicate-test-config')

    with pytest.raises(OKSValueError):
        find_session(test_config_root, 'non-existing-test-config')


def test_get_many_object_by_object_id(test_config_root):
    sessions = get_many_object(test_config_root, object_id="test-config")
    assert len(sessions) == 1
    assert sessions[0].attrib['id'] == "test-config"
    assert sessions[0].attrib['class'] == "Session"

    # a bit of a weird case? We have 2 objects with the same id...
    sessions = get_many_object(test_config_root, object_id="duplicate-test-config")
    assert len(sessions) == 2
    assert sessions[0].attrib['id'] == "duplicate-test-config"
    assert sessions[1].attrib['id'] == "duplicate-test-config"
    assert sessions[0].attrib['class'] == "Session"
    assert sessions[1].attrib['class'] == "Session"

    with pytest.raises(OKSValueError):
        get_many_object(test_config_root, object_id="non-existing-test-config")


def test_get_many_object_by_class_name(test_config_root):
    avx = get_many_object(test_config_root, class_name="AVXAbsRunSumProcessor")
    assert len(avx) == 1
    assert avx[0].attrib['id'] == "tpg-absrs-proc"
    assert avx[0].attrib['class'] == "AVXAbsRunSumProcessor"

    sessions = get_many_object(test_config_root, class_name="Session")
    assert len(sessions) == 3
    ids = [session.attrib['id'] for session in sessions]
    assert all([session.attrib['class'] == "Session" for session in sessions])
    assert "test-config" in ids
    assert "duplicate-test-config" in ids
    ids.remove("duplicate-test-config")
    assert "duplicate-test-config" in ids

    with pytest.raises(OKSValueError):
        get_many_object(test_config_root, class_name="NotASession")


def test_get_many_object_by_object_id_and_class_name(test_config_root):
    avx = get_many_object(test_config_root, class_name="AVXAbsRunSumProcessor", object_id="tpg-absrs-proc")
    assert len(avx) == 1
    assert avx[0].attrib['id'] == "tpg-absrs-proc"
    assert avx[0].attrib['class'] == "AVXAbsRunSumProcessor"

    sessions = get_many_object(test_config_root, class_name="Session", object_id="test-config")
    assert len(sessions) == 1
    assert sessions[0].attrib['id'] == "test-config"
    assert sessions[0].attrib['class'] == "Session"

    with pytest.raises(OKSValueError):
        get_many_object(test_config_root, class_name="NotASession", object_id="test-config")

    with pytest.raises(OKSValueError):
        get_many_object(test_config_root, class_name="Session", object_id="not-a-test-config")


def test_get_one_relation_by_class(test_config_root):
    session = find_session(test_config_root, 'test-config')
    segment = get_one_relation_by_class(test_config_root, session, name="Segment")
    assert segment is not None
    assert segment.attrib['id'] == 'root-segment'
    assert segment.attrib['class'] == 'Segment'

    with pytest.raises(OKSValueError):
        get_one_relation_by_class(test_config_root, session, name="NotASegment")

    with pytest.raises(OKSValueError):
        get_one_relation_by_class(test_config_root, session, name="Variable")


def test_get_one_relation_by_name(test_config_root):
    session = find_session(test_config_root, 'test-config')
    segment = get_one_relation_by_name(test_config_root, session, name="segment")
    assert segment is not None
    assert segment.attrib['id'] == 'root-segment'
    assert segment.attrib['class'] == 'Segment'

    with pytest.raises(OKSValueError):
        get_one_relation_by_class(test_config_root, session, name="not-a-segment")

    with pytest.raises(OKSValueError):
        get_one_relation_by_class(test_config_root, session, name="environment")


def test_get_many_relation_by_class(test_config_root):
    session = find_session(test_config_root, 'test-config')
    root_segment = get_one_relation_by_class(test_config_root, session, name="Segment")
    segments = get_many_relation_by_class(test_config_root, root_segment, name="Segment")

    assert len(segments) == 4
    classes = [segment.attrib['class'] for segment in segments]
    assert all([class_ == 'Segment' for class_ in classes])
    ids = [segment.attrib['id'] for segment in segments]
    assert 'df-segment' in ids
    assert 'ru-segment' in ids
    assert 'trg-segment' in ids
    assert 'hsi-fake-segment' in ids

    with pytest.raises(OKSValueError):
        get_many_relation_by_class(test_config_root, root_segment, name="NotASegment")


def test_get_many_relation_by_name(test_config_root):
    session = find_session(test_config_root, 'test-config')
    root_segment = get_one_relation_by_name(test_config_root, session, name="segment")
    segments = get_many_relation_by_name(test_config_root, root_segment, name="segments")

    assert len(segments) == 4
    classes = [segment.attrib['class'] for segment in segments]
    assert all([class_ == 'Segment' for class_ in classes])
    ids = [segment.attrib['id'] for segment in segments]
    assert 'df-segment' in ids
    assert 'ru-segment' in ids
    assert 'trg-segment' in ids
    assert 'hsi-fake-segment' in ids

    with pytest.raises(OKSValueError):
        get_many_relation_by_name(test_config_root, root_segment, name="not-segments")


def test_get_one_attribute(test_config_root):
    session = find_session(test_config_root, 'test-config')
    controller_log_level = get_one_attribute(test_config_root, session, name="controller_log_level")
    assert controller_log_level is not None
    assert controller_log_level.attrib['name'] == 'controller_log_level'
    assert controller_log_level.attrib['val'] == 'INFO'

    with pytest.raises(OKSValueError):
        get_one_attribute(test_config_root, session, name="not-controller_log_level")



def test_does_not_accept_include(ehn1_daqconfig_sessions):
    for file_path in ehn1_daqconfig_sessions(False).values():
        tree = parse(file_path)
        root = tree.getroot()
        assert check_for_data_includes(root)

    for file_path in ehn1_daqconfig_sessions(True).values():
        tree = parse(file_path)
        root = tree.getroot()
        assert not check_for_data_includes(root)


def test_get(test_config_root):
    session = find_session(test_config_root, 'test-config')

    controller_log_level = get(test_config_root, session, name="controller_log_level")
    assert controller_log_level is not None
    assert controller_log_level.attrib['name'] == 'controller_log_level'
    assert controller_log_level.attrib['val'] == 'INFO'

    detector_configuration = get(test_config_root, session, name="detector_configuration")
    assert detector_configuration is not None
    assert detector_configuration.attrib['id'] == 'dummy-detector'
    assert detector_configuration.attrib['class'] == 'DetectorConfig'

    environment = get(test_config_root, session, name="environment")
    assert len(environment) == 5
    ids = [env.attrib['id'] for env in environment]
    classes = [env.attrib['class'] for env in environment]
    assert 'local-env-ers-verb' in ids
    assert 'local-env-ers-info' in ids
    assert 'local-env-ers-warning' in ids
    assert 'local-env-ers-error' in ids
    assert 'local-env-ers-fatal' in ids
    assert all([class_ == 'Variable' for class_ in classes])
