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
    get,
)


def test_get_one_object_by_object_name(test_config_root):
    session = get_one_object(test_config_root, object_name="test-config")
    assert session is not None
    assert session['__name'] == "test-config@Session"

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, object_name="non-existing-test-config")


def test_get_one_object_by_class_name(test_config_root):
    avx = get_one_object(test_config_root, class_name="AVXAbsRunSumProcessor")
    assert avx is not None
    assert avx['__name'] == "tpg-absrs-proc@AVXAbsRunSumProcessor"

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, class_name="NotASession")


def test_get_one_object_by_object_name_and_class_name(test_config_root):
    avx = get_one_object(test_config_root, class_name="AVXAbsRunSumProcessor", object_name="tpg-absrs-proc")
    assert avx is not None
    assert avx['__name'] == "tpg-absrs-proc@AVXAbsRunSumProcessor"

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, class_name="Session", object_name="bananas")

    with pytest.raises(OKSValueError):
        get_one_object(test_config_root, class_name="Bananas", object_name="tpg-absrs-proc")


def test_find_session(test_config_root):
    session = find_session(test_config_root, 'test-config')
    assert session is not None
    assert session['__name'] == 'test-config@Session'

    with pytest.raises(OKSValueError):
        find_session(test_config_root, 'non-existing-test-config')


def test_get_many_object_by_object_name(test_config_root):
    sessions = get_many_object(test_config_root, object_name="test-config")
    assert len(sessions) == 1
    assert sessions[0]['__name'] == "test-config@Session"

    with pytest.raises(OKSValueError):
        get_many_object(test_config_root, object_name="non-existing-test-config")


def test_get_many_object_by_class_name(test_config_root):
    avx = get_many_object(test_config_root, class_name="AVXAbsRunSumProcessor")
    assert len(avx) == 1
    assert avx[0]['__name']  == "tpg-absrs-proc@AVXAbsRunSumProcessor"

    sessions = get_many_object(test_config_root, class_name="Session")
    assert len(sessions) == 2
    ids = [session['__name'] for session in sessions]
    assert all([session['__name'].endswith("@Session") for session in sessions])
    assert "test-config@Session" in ids
    assert "test-config2@Session" in ids

    with pytest.raises(OKSValueError):
        get_many_object(test_config_root, class_name="NotASession")


def test_get_many_object_by_object_name_and_class_name(test_config_root):
    avx = get_many_object(test_config_root, class_name="AVXAbsRunSumProcessor", object_name="tpg-absrs-proc")
    assert len(avx) == 1
    assert avx[0]['__name'] == "tpg-absrs-proc@AVXAbsRunSumProcessor"

    sessions = get_many_object(test_config_root, class_name="Session", object_name="test-config")
    assert len(sessions) == 1
    assert sessions[0]['__name'] == "test-config@Session"

    with pytest.raises(OKSValueError):
        get_many_object(test_config_root, class_name="NotASession", object_name="test-config")

    with pytest.raises(OKSValueError):
        get_many_object(test_config_root, class_name="Session", object_name="not-a-test-config")


def test_get_one_relation_by_class(test_config_root):
    session = find_session(test_config_root, 'test-config')
    segment = get_one_relation_by_class(test_config_root, session, class_name="Segment")
    assert segment is not None
    assert segment['__name'] == "root-segment@Segment"

    with pytest.raises(OKSValueError):
        get_one_relation_by_class(test_config_root, session, class_name="NotASegment")

    with pytest.raises(OKSValueError):
        get_one_relation_by_class(test_config_root, session, class_name="Variable")


def test_get_one_relation_by_name(test_config_root):
    session = find_session(test_config_root, 'test-config')
    segment = get_one_relation_by_name(test_config_root, session, object_name="segment")
    assert segment is not None
    assert segment['__name'] == "root-segment@Segment"

    with pytest.raises(OKSValueError):
        get_one_relation_by_name(test_config_root, session, object_name="not-a-segment")

    with pytest.raises(OKSValueError):
        get_one_relation_by_name(test_config_root, session, object_name="environment")


def test_get_many_relation_by_class(test_config_root):
    session = find_session(test_config_root, 'test-config')
    root_segment = get_one_relation_by_class(test_config_root, session, class_name="Segment")
    segments = get_many_relation_by_class(test_config_root, root_segment, class_name="Segment")

    assert len(segments) == 4
    classes = [segment['__name'].split('@')[1] for segment in segments]
    assert all([class_ == 'Segment' for class_ in classes])
    ids = [segment['__name'] for segment in segments]
    assert 'df-segment@Segment' in ids
    assert 'ru-segment@Segment' in ids
    assert 'trg-segment@Segment' in ids
    assert 'hsi-fake-segment@Segment' in ids

    with pytest.raises(OKSValueError):
        get_many_relation_by_class(test_config_root, root_segment, class_name="NotASegment")


def test_get_many_relation_by_name(test_config_root):
    session = find_session(test_config_root, 'test-config')
    root_segment = get_one_relation_by_name(test_config_root, session, object_name="segment")
    segments = get_many_relation_by_name(test_config_root, root_segment, object_name="segments")

    assert len(segments) == 4
    classes = [segment['__name'].split('@')[1] for segment in segments]
    assert all([class_ == 'Segment' for class_ in classes])
    ids = [segment['__name'] for segment in segments]
    assert 'df-segment@Segment' in ids
    assert 'ru-segment@Segment' in ids
    assert 'trg-segment@Segment' in ids
    assert 'hsi-fake-segment@Segment' in ids

    with pytest.raises(OKSValueError):
        get_many_relation_by_name(test_config_root, root_segment, object_name="not-segments")


def test_get_one_attribute(test_config_root):
    session = find_session(test_config_root, 'test-config')
    controller_log_level = get_one_attribute(test_config_root, session, attribute_name="controller_log_level")
    assert controller_log_level == 'INFO'

    with pytest.raises(OKSValueError):
        get_one_attribute(test_config_root, session, attribute_name="not-controller_log_level")


def test_get(test_config_root):
    session = find_session(test_config_root, 'test-config')

    controller_log_level = get(test_config_root, session, object_name="controller_log_level")
    assert controller_log_level == 'INFO'

    detector_configuration = get(test_config_root, session, object_name="detector_configuration")
    assert detector_configuration is not None
    assert detector_configuration['__name'] == 'dummy-detector@DetectorConfig'

    environment = get(test_config_root, session, object_name="environment")
    assert len(environment) == 5
    names   = [env['__name'].split('@')[0] for env in environment]
    classes = [env['__name'].split('@')[1] for env in environment]
    assert 'local-env-ers-verb' in names
    assert 'local-env-ers-info' in names
    assert 'local-env-ers-warning' in names
    assert 'local-env-ers-error' in names
    assert 'local-env-ers-fatal' in names
    assert all([class_ == 'Variable' for class_ in classes])
