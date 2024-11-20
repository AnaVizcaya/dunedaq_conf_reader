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
from offline_conf_reader.oks_data_extractor import DUNEDAQConfDataExtractor
cde = DUNEDAQConfDataExtractor("path/to/file", "session_name")
```

You can now access the variables:
 - `buffer`: object
 - `ac_couple`: object
 - `pulse_dac`: object
 - `pulser`: object
 - `baseline`: object
 - `gain`: object
 - `leak`: object
 - `leak_10x`: object
 - `peak_time`: object
 - `enable_femb_fake_data`: object
 - `test_cap`: object
 - `APAs`: list of int
 - `FEMBs`: list of int
 - `pulse_period`: object
 - `phase_group`: object
 - `phases`: object

```python
>> print(cde.buffer)
>> 1
```

## Bash usage
After `pip install`'ing above, you can do:
```bash
offline-conf-reader /path/to/file session_name variable0_name variable1_name...
```

For example:
```bash
offline-conf-reader /path/to/file session_name buffer
0
offline-conf-reader /path/to/file session_name buffer ac_couple
0
1
```

## Developper
... Please run `pytest` everytime you make a modification and make sure it passes!
