import argparse
from mzml2gnps.main import pipline_test
    # Define the argument parser
def main():
    parser = argparse.ArgumentParser(description='Process mzML files for GNPS molecular networking.')
    parser.add_argument('-f','--file_path', type=str, help='Input mzML file path or folder path containing mzML files')
    parser.add_argument('-o','--output_path', type=str, help='Output folder path')
    parser.add_argument('--precmz', type=str, default=None, help='CSV file path for list of precursor m/z values')
    parser.add_argument('--rt', type=str, default=None, help='CSV file path for list of retention times')
    parser.add_argument('--precmz_tolerance', type=float, default=20, help='Precursor m/z tolerance')
    parser.add_argument('--rt_tolerance', type=float, default=0.5, help='Retention time tolerance')
    parser.add_argument('--precinty_thre', type=float, default=0, help='Precursor intensity threshold')
    parser.add_argument('--csv', type=str, default=None, help='CSV file path including precmz and rt columns, default is None')
    parser.add_argument('--correct', action='store_true', help='Correct precursors, default is False (use flag to enable)')
    parser.add_argument('--merge', action='store_true', help='Merge spectra, default is False (use flag to enable)')
    args = parser.parse_args()

    pipline_test(args)

if __name__ == '__main__':
    main()