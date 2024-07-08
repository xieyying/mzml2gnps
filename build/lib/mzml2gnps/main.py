import os
import pandas as pd
from mzml2gnps.methods import *
from .test import path_check
def pipline_test(args):
    path_check(args.output_path)
        

    if os.path.isdir(args.file_path):
        for file in os.listdir(args.file_path):
            if file.endswith('.mzML'):
                file_path = os.path.join(args.file_path, file)
                output_path = os.path.join(args.output_path, file)
                # If a combined CSV is provided, use it to extract precmz and rt DataFrames
                if args.csv:
                     precmz, rt,RTstart,RTend = read_csv_to_df(args.csv)
                else:
                    # Convert CSV file paths to DataFrames if individual paths are provided
                    precmz = args.precmz
                    rt = args.rt
                    RTstart = None
                    RTend = None
                pipline(file_path, output_path, precmz, rt,RTstart,RTend, args.precmz_tolerance, args.rt_tolerance, args.precinty_thre, args.correct, args.merge)
        exit()
    else:

       # If a combined CSV is provided, use it to extract precmz and rt DataFrames
        if args.csv:
            precmz, rt,RTstart,RTend = read_csv_to_df(args.csv)
        else:
            # Convert CSV file paths to DataFrames if individual paths are provided
            precmz = args.precmz
            rt = args.rt
            RTstart = None
            RTend = None

        #不存在output_path文件夹则创建

        out_path = os.path.join(args.output_path, os.path.basename(args.file_path))
            
        # Call the pipeline function with the DataFrames
        pipline(args.file_path, out_path, precmz, rt,RTstart,RTend, args.precmz_tolerance, args.rt_tolerance, args.precinty_thre, args.correct, args.merge)
