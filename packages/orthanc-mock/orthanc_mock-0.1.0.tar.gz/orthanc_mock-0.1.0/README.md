# orthanc-mock
__Mock for the python orthanc plugin intended for development.__

This library is intended to be used while developing python scripts
with the Python plugin for Orthanc. It simply provides the 
functions/classes/enums signatures for the autocomplete.

## Installation
```bash
pip install orthanc-mock
```

## Usage


Note that the `orthanc-mock` library should be installed as a
__dev__ dependency so that it does not interfere while running inside Orthanc.

```python
import orthanc

# Functions are accessible
orthanc.RegisterRestCallback()
orthanc.RestApiGet()
...

# Classes are as well
orthanc.DicomInstance.GetInstanceMetadata()
orthanc.DicomInstance.HasInstanceMetadata()
...

# And the enum
orthanc.ChangeType.NEW_STUDY
orthanc.ChangeType.ORTHANC_STOPPED
...
```

## Credits
The `orthanc.py` has been generated from the `data/python-sdk.txt` file,
which is from the [Python Orthanc Plugin](https://github.com/orthanc-server/orthanc-setup-samples/blob/master/python-samples/python-sdk.txt)