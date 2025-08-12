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

### Command Line Arguments

- `--file_path`: Input mzML file path or folder path containing mzML files (required).
- `--output_path`: Output folder path (required).
- `--precmz`: List of precursor m/z values (optional).
- `--rt`: List of retention times (optional).
- `--precmz_tolerance`: Precursor m/z tolerance (default: 20).
- `--rt_tolerance`: Retention time tolerance (default: 0.5).
- `--precinty_thre`: Precursor intensity threshold (default: 0).
- `--csv`: CSV file path including `precmz` and `rt` columns (optional).
- `--correct`: Flag to enable precursor correction (default: False).
- `--merge`: Flag to enable spectra merging (default: False).

### Example

```shell
python mzml2gnps.py --file_path input.mzML --output_path /path/to/output --correct

This command processes the input.mzML file, corrects precursors and saves the processed spectra to the specified output path.

Development
This script was developed using Python and relies on the pyopenms library for handling mzML files and MS data processing.

Contributing
If you have suggestions for how mzml2gnps could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

For more, check out the Contributing Guide.

License
MIT © Yunying Xie