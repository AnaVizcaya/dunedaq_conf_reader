from dataclasses import dataclass
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

    def extract():
        pass
