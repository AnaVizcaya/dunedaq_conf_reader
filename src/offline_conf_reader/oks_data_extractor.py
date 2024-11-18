from dataclasses import dataclass, Field, fields
from pathlib import Path

@dataclass
class OKSDataExtractor:
    session_name:str
    oks_file_path: Path
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

    def extract(self):
        pass

    def get_variables(self) -> list[Field]:

        data = []
        for field in fields(self):
            if field.name == 'session_name' or field.name == 'oks_file_path':
                continue
            data += [field]

        return data
