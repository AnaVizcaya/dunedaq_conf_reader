# A python-native reader for the DUNE-DAQ OKS data

## Installation
```bash
git clone https://github.com/plasorak/offline_conf_reader.git
cd offline_conf_reader
pip install .
```

## Python usage
 - Import the `DUNEDAQConfDataExtractor`,
 - Create an instance of that class, with the path of the file you are reading, and the `Session` identifier.

```python
from offline_conf_reader.dunedaq_conf_data_extractor import DUNEDAQConfDataExtractor
cde = DUNEDAQConfDataExtractor("path/to/file", "session_name")
```

You can now access (some of) the  variables:
 - `buffer`: Not accessible
 - `ac_couple`: `dict[str,bool]`
 - `pulse_dac`: Not accessible
 - `pulser`: `dict[str,bool]`
 - `baseline`: `dict[str,int]`
 - `gain`: `dict[str,int]`
 - `leak`: Not accessible
 - `leak_10x`: `dict[str,bool]`
 - `peak_time`: `dict[str,int]`
 - `enable_femb_fake_data`: Not accessible
 - `test_cap`: `dict[str,bool]`
 - `APAs`: `list[int]`
 - `FEMBs`: Not accessible
 - `pulse_period`: `dict[str,int]`
 - `phase_group`: Not accessible
 - `phases`: Not accessible

```python
>> print(cde.baseline)
>> {'crp4-wiec_femb0': 2, 'crp4-wiec_femb1': 2, 'crp4-wiec_femb2': 2, 'crp4-wiec_femb3': 2, 'crp5-wiec_femb0': 2, 'crp5-wiec_femb1': 2, 'crp5-wiec_femb2': 2, 'crp5-wiec_femb3': 2}
```

## Bash usage
After `pip install`'ing above, you can do:
```bash
offline-conf-reader /path/to/file session_name variable0_name variable1_name...
```

For example:
```bash
offline-conf-reader /path/to/file session_name ac_couple
crp4-wiec_femb0: False
crp4-wiec_femb1: False
crp4-wiec_femb2: False
crp4-wiec_femb3: False
crp5-wiec_femb0: False
crp5-wiec_femb1: False
crp5-wiec_femb2: False
crp5-wiec_femb3: False
offline-conf-reader  /path/to/file session_name ac_couple baseline
crp4-wiec_femb0: False
crp4-wiec_femb1: False
crp4-wiec_femb2: False
crp4-wiec_femb3: False
crp5-wiec_femb0: False
crp5-wiec_femb1: False
crp5-wiec_femb2: False
crp5-wiec_femb3: False
crp4-wiec_femb0: 2
crp4-wiec_femb1: 2
crp4-wiec_femb2: 2
crp4-wiec_femb3: 2
crp5-wiec_femb0: 2
crp5-wiec_femb1: 2
crp5-wiec_femb2: 2
crp5-wiec_femb3: 2
```

## Developper
... Please run `pytest` everytime you make a modification and make sure it passes!
