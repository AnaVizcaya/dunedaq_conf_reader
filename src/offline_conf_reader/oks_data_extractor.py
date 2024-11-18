from dataclasses import dataclass, Field, fields
from pathlib import Path
from defusedxml.ElementTree import parse


def check_for_data_includes(root):
    for child in root:
        if child.tag != 'include':
            continue
        for include_file in child:
            if include_file.tag != 'file':
                continue
            if include_file.attrib['path'].endswith('.schema.xml'):
                continue
            return True

    return False

def find_session(root, session_name):
    for child in root:
        if child.tag == 'obj' and child.attrib['class'] == "Session" and child.attrib['id'] == session_name:
            return child


def get(root, start_obj, object_name=None, class_name=None):

    if object_name is None and class_name is None:
        raise ValueError('Either \'object_name\' or \'class_name\' must be provided')

    for child in start_obj:
        if class_name is not None and child.attrib.get('class') is not None and child.attrib.get('class') != class_name:
            continue

        if object_name is not None and child.attrib.get('name') is not None and child.attrib.get('name') != object_name:
            continue

        if child.tag == 'attr':
            return child

        if child.tag == 'rel':
            for obj in root.findall('obj'):
                if obj.attrib['id'] != child.attrib['id']:
                    continue
                return obj
    raise ValueError(f'Could not find object with name \'{object_name}\' or class \'{class_name}\' in {start_obj.attrib["id"]}, which is composed of: {[s.attrib["name"] for s in start_obj]}')



@dataclass
class OKSDataExtractor:
    oks_file_path: Path
    session_name:str
    buffer: object = None
    ac_couple: object = None
    pulse_dac: object = None
    pulser: object = None
    baseline: object = None
    gain: object = None
    leak: object = None
    leak_10x: object = None
    peak_time: object = None
    enable_femb_fake_data: object = None
    test_cap: object = None
    APAs: list[int] = None
    FEMBs: list[int] = None
    pulse_period: object = None
    phase_group: object = None
    phases: object = None

    def __post_init__(self):
        if self.oks_file_path == 'dummy':
            return

        tree = parse(self.oks_file_path)
        root = tree.getroot()

        if check_for_data_includes(root):
            raise RuntimeError('Include files are not supported, the configuration was not consolidated!')

        session = find_session(root, self.session_name)
        print(session.attrib)
        for session_child in session:
            print(session_child.tag, session_child.attrib)

        print(get(root, session, object_name='data_rate_slowdown_factor').attrib)

        print(get(root, session, object_name='segment').attrib)



    def get_variables(self) -> list[Field]:

        data = []
        for field in fields(self):
            if field.name == 'session_name' or field.name == 'oks_file_path':
                continue
            data += [field]

        return data
