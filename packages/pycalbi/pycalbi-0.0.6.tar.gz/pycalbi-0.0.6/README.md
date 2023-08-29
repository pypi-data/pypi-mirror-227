# CALBI: Concurrent Automation Library for Bots in Intelmq

## Description

CALBI is a library designed to manage concurrent execution of the same Intelmq bot instances when dealing with rate-limited APIs or applications.

## Features

- Dynamic rate-limiting.
- Asynchronous execution of bot tasks.
- Configurable parameters for bot instances
  
## Requirements

- Python >= 3.6
- Intelmq >= 2.0
- Redis

## Installation

```
bash
pip install pycalbi
```
Or from source:
```
git clone https://github.com/CSIRTAmericas/CALBI.git
cd CALBI
python setup.py install

```
## Use

```
from pycalbi import Calbi
```

Take a look at boyt.py to take a look in a full bot example.

## Contributing

Pull requests are welcome. Please make sure to update tests as appropriate.

Note: If you paste this into a README.md file, the nested code blocks should render correctly on GitHub.
