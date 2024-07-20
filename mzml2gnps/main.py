import os
from mzml2gnps.methods import pipeline, read_csv_to_df
from .test import path_check

def pipeline_test(args):
    """
    Processes mass spectrometry data files (.mzML) using parameters provided in args.

    Parameters:
    - args: An object containing all necessary parameters including file paths, tolerances, and flags for correction and merging.
    """
    path_check(args.output_path)

    # Ensure the output directory exists
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    def process_file(file_path, output_path):
        """
        Helper function to process a single file.
        """
        if args.csv:
            precmz, rt, RTstart, RTend = read_csv_to_df(args.csv)
        else:
            precmz, rt = args.precmz, args.rt
            RTstart, RTend = None, None

        pipeline(file_path, output_path, precmz, rt, RTstart, RTend, args.precmz_tolerance, args.rt_tolerance, args.precinty_thre, args.correct, args.merge)

    if os.path.isdir(args.file_path):
        for file in os.listdir(args.file_path):
            if file.endswith('.mzML'):
                file_path = os.path.join(args.file_path, file)
                output_path = os.path.join(args.output_path, file)
                process_file(file_path, output_path)
    else:
        out_path = os.path.join(args.output_path, os.path.basename(args.file_path))
        process_file(args.file_path, out_path)