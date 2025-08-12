# mzml2gnps

`mzml2gnps` is a Python script designed for processing mzML files for GNPS (Global Natural Products Social Molecular Networking) molecular networking. It provides functionalities for loading mzML experiments, correcting precursor m/z values, merging spectra according to rt, precusor and similarity of MS2 spectra, filtering MS2 spectra based on various criteria, and exporting the processed spectra to a new mzML file.

## Features

- **Load mzML Experiment**: Load an mzML file and create an MSExperiment object.
- **Correct Precursors**: Correct the precursor m/z values to the highest intensity MS1 peak within a specified tolerance.
- **Merge Spectra**: Merge spectra based on retention times, precusors and similarities of MS2 spectra.
- **Filter MS2 Spectra**: Filter MS2 spectra based on precursor m/z, retention time, and precursor intensity threshold.
- **Export to mzML**: Export the filtered MS2 spectra to a new mzML file.

## Requirements

- Python 3.10.13
- pandas 2.0.3
- pyopenms 3.1.0-pre-HEAD-2023-10-13

## Installation

To install [`mzml2gnps`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FUsers%2Fxyy%2FDesktop%2Fpython%2Fmzml2gnps%2FREADME.md%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A0%2C%22character%22%3A0%7D%5D "../mzml2gnps/README.md"), ensure you have Python 3.10 or later installed. Then, follow these steps:

1. Install the package directly from PyPI:

```shell
pip install mzml2gnps
```

2. If you want to install from the source, first clone the repository:

```shell
git clone https://github.com/yourusername/mzml2gnps.git
cd mzml2gnps
```

3. Then, use the following command to install:

```shell
pip install .
```

This will automatically handle the dependencies listed in `pyproject.toml`.
## Usage

The script can be executed from the command line with various arguments to specify the input and output paths, filtering criteria, and whether to perform precursor correction and spectra merging.

### Example

```shell
python mzml2gnps.py -i input.mzML -o /path/to/output --correct
```
This command processes the input.mzML file, corrects precursors and saves the processed spectra to the output path.

```shell
python mzml2gnps.py -i /path/to/input -o /path/to/output --correct
```
This command processes all the files endwith .mzML in the input folder, corrects precursors and saves the processed spectra to the output path.

### Command Line Arguments

The script supports the following command-line arguments:

#### General Options:
- `-h, --help`  
  Show the help message and exit.
- `--version`  
  Show the program's version number and exit.

#### Input and Output:
- `-i INPUT_PATH, --input_path INPUT_PATH`  
  Specify the input mzML file path or folder containing mzML files.
- `-o OUTPUT_PATH, --output_path OUTPUT_PATH`  
  Specify the output folder path.

#### Processing Options:
- `--correct`  
  Enable precursor correction (default is `False`).
- `--merge`  
  Enable spectra merging (default is `False`).

#### Filtering Criteria:
- `--precmz PRECMZ`  
  Path to a CSV file containing a list of precursor m/z values.
- `--rt RT`  
  Path to a CSV file containing a list of retention times.
- `--precmz_tolerance PRECMZ_TOLERANCE`  
  Precursor m/z tolerance (in ppm).
- `--rt_tolerance RT_TOLERANCE`  
  Retention time tolerance (in seconds).
- `--precinty_thre PRECINTY_THRE`  
  Precursor intensity threshold.

#### Combined Input:
- `--csv CSV`  
  Path to a CSV file containing both precursor m/z and retention time columns (default is `None`).

Development
This script was developed using Python and relies on the pyopenms library for handling mzML files and MS data processing.

Contributing
If you have suggestions for how mzml2gnps could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

License
MIT © Yunying Xie