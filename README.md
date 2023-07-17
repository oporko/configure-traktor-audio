# configure-traktor-audio
Small Python script for configuring Traktor Audio 6 in Linux

### Install prerequisite modules
```bash
pip install -r requirements.txt
```

### Usage

The Python v3 command may be python on your system, replace python3 in the below examples with python if this is the case.

#### Show help message
```bash
python3 configure-traktor-audio-6.py
```

#### Turn off thru for channel a
```bash
python3 configure-traktor-audio-6.py --channel a --thru off
```

#### Turn off phono for channel b
```bash
python3 configure-traktor-audio-6.py --channel b --phono off
```

#### Turn on thru and phono for both channels
```bash
python3 configure-traktor-audio-6.py --channel a b --thru on --phono on
```

#### Turn off thru and phono for both channels and suppress output
```bash
python3 configure-traktor-audio-6.py --channel a b --thru off --phono off --quiet
```

#### As above, but with argument short forms
```bash
python3 configure-traktor-audio-6.py -c a b -t off -p off -q
```
