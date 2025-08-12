import os
from mzml2gnps.methods import read_csv_to_df, pipeline
def pipeline_test(args):
    os.makedirs(args.output_path, exist_ok=True)

    # If a combined CSV is provided, use it to extract precmz and rt DataFrames
    if args.csv:
        precmz, rt, RTstart, RTend = read_csv_to_df(args.csv)
    else:
        # Convert CSV file paths to DataFrames if individual paths are provided
        precmz = args.precmz
        rt = args.rt
        RTstart = None
        RTend = None
        
    mzml_files = []

    if os.path.isdir(args.input_path):
        #walk through the directory
        for root, dirs, files in os.walk(args.input_path):
            for file in files:
                if file.endswith('.mzML'):
                    mzml_files.append(os.path.join(root, file))
    else:
        mzml_files.append(args.input_path)
    
    for file in mzml_files:
        if file.endswith('.mzML'):
            output_path = os.path.join(args.output_path, os.path.basename(file))
            # Call the pipeline function with the DataFrames
            pipeline(file, output_path, precmz, rt, RTstart, RTend, args.precmz_tolerance, args.rt_tolerance, args.precinty_thre, args.correct, args.merge)

