from dataclasses import dataclass, Field, fields
import json
from pathlib import Path
import logging
from dunedaq_conf_reader.oks_utils import find_session, get, get_applications
detector_types = ['CRP', 'APA']

@dataclass
class DUNEDAQConfDataExtractor:
    oks_file_path: Path
    session_name:str
    buffering            : dict[str,int] = None
    ac_couple            : dict[str,bool] = None
    pulse_dac            : object = None
    pulser               : dict[str,bool] = None
    baseline             : dict[str,int]  = None
    gain                 : dict[str,int]  = None
    leak                 : object = None
    leak_10x             : dict[str,bool] = None
    peak_time            : dict[str,int]  = None
    enable_femb_fake_data: object = None
    test_cap             : dict[str,bool] = None
    APAs                 : list[int] = None
    FEMBs                : object = None
    pulse_period         : dict[str,int]  = None
    phase_group          : object = None
    phases               : object = None

    def __post_init__(self):
        if self.oks_file_path == None or self.session_name == None:
            return

        self.ac_couple    = {}
        self.buffering    = {}
        self.pulser       = {}
        self.baseline     = {}
        self.gain         = {}
        self.leak_10x     = {}
        self.peak_time    = {}
        self.test_cap     = {}
        self.pulse_period = {}
        self.APAs         = []

        conf_data = {}
        with open(self.oks_file_path) as f:
            conf_data = json.load(f)

        session = find_session(conf_data, self.session_name)
        logging.debug(f'{session=}')
        wiec_applications = get_applications(
            conf_data,
            session,
            application_class_name="WIECApplication"
        )
        logging.info(f'Found {len(wiec_applications)} WIEC applications')

        for wiec_application in wiec_applications:
            wiec_application_name = wiec_application['__name']
            logging.info(f'Processing WIEC application: \'{wiec_application_name.split("@")[0]}\'')

            wib_module_conf = get(conf_data, wiec_application, "wib_module_conf")
            wib_settings = get(conf_data, wib_module_conf, "settings")

            self.pulser[wiec_application_name] = get(conf_data, wib_settings, "pulser")
            logging.info(f'\'Pulser\': {self.pulser[wiec_application_name]}')

            wib_pulser_setting = get(conf_data, wib_settings, "wib_pulser")
            self.pulse_period[wiec_application_name] = get(conf_data, wib_pulser_setting, "pulse_period")
            logging.debug(f'\'Pulser period\': {self.pulse_period[wiec_application_name]}')

            fembs =  [get(conf_data, wib_settings, "femb0")]
            fembs += [get(conf_data, wib_settings, "femb1")]
            fembs += [get(conf_data, wib_settings, "femb2")]
            fembs += [get(conf_data, wib_settings, "femb3")]

            self.extract_femb_variables(conf_data, self.leak_10x , "leak_10x" , fembs, wiec_application_name)
            self.extract_femb_variables(conf_data, self.ac_couple, "ac_couple", fembs, wiec_application_name)
            self.extract_femb_variables(conf_data, self.peak_time, "peak_time", fembs, wiec_application_name)
            self.extract_femb_variables(conf_data, self.baseline , "baseline" , fembs, wiec_application_name)
            self.extract_femb_variables(conf_data, self.test_cap , "test_cap" , fembs, wiec_application_name)
            self.extract_femb_variables(conf_data, self.buffering, "buffering", fembs, wiec_application_name)


        ru_applications = get_applications(
            conf_data,
            session,
            application_class_name="ReadoutApplication"
        )
        logging.info(f'Found {len(ru_applications)} RU applications')
        ru_applications = []
        for ru_application in ru_applications:
            contains = get(conf_data, ru_application, "contains")
            connections = [contain.attrib['id'].upper().replace('_', "-") for contain in contains]
            for connection in connections:
                for i in connection.split('-'):
                    for detector_type in detector_types:
                        if detector_type in i:
                            self.APAs += [i]

    def extract_femb_variables(self, conf_data, field_to_fill, name, fembs, prefix):
        for i, femb in enumerate(fembs):
            field_to_fill[prefix+f"_femb{i}"] = get(conf_data, femb, name)
            logging.info(f'\'{name}\' for \'femb{i}\': {field_to_fill[prefix+f"_femb{i}"]}')


    def get_variables(self) -> list[Field]:

        data = []
        for field in fields(self):
            if field.name == 'session_name' or field.name == 'oks_file_path':
                continue
            data += [field]

        return data
