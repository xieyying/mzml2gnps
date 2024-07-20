from typing import Tuple, List, Optional
import pandas as pd
import pyopenms as oms

def load_experiment(file_path: str) -> oms.MSExperiment:
    """
    Loads an experiment from a given file path.

    Parameters:
    - file_path (str): The path to the .mzML file to be loaded.

    Returns:
    - oms.MSExperiment: The loaded MSExperiment object.
    """
    exp = oms.MSExperiment()
    try:
        oms.MzMLFile().load(file_path, exp)
    except Exception as e:
        print(f"Failed to load experiment from {file_path}: {e}")
        raise
    return exp

def correct_precursors(exp: oms.MSExperiment, mz_tolerance: float = 0.5, ppm: bool = False) -> None:
    """
    Corrects the precursor m/z values in the experiment to the highest intensity MS1 peak within a given tolerance.

    Parameters:
    - exp (oms.MSExperiment): The experiment to correct.
    - mz_tolerance (float): The m/z tolerance for correction.
    - ppm (bool): Whether the tolerance is in parts per million.

    Returns:
    - Tuple[List[float], List[float], List[float]]: Lists of delta m/z values, corrected m/z values, and retention times.
    """
    delta_mzs, mzs, rts = [], [], []
    corr = oms.PrecursorCorrection()
    corr.correctToHighestIntensityMS1Peak(exp, mz_tolerance, ppm, delta_mzs, mzs, rts)


def merge_spectra(exp: oms.MSExperiment) -> None:
    """
    Merges spectra with the same precursor in an experiment.

    Parameters:
    - exp (oms.MSExperiment): The experiment whose spectra are to be merged.
    """
    mg = oms.SpectraMerger()
    try:
        mg.mergeSpectraPrecursors(exp)
    except Exception as e:
        print(f"Failed to merge spectra: {e}")
        raise    

def filter_ms2(exp: oms.MSExperiment, 
               precursor_mz: Optional[List[float]] = None, 
               retention_time: Optional[List[float]] = None, 
               rt_start: Optional[List[float]] = None,
               rt_end: Optional[List[float]] = None,
               precursor_mz_tolerance: float = 20, 
               rt_tolerance: float = 0.5, 
               precursor_intensity_threshold: float = 0) -> List[oms.MSSpectrum]:
    """
    Filters MS2 spectra based on precursor m/z, retention time, and precursor intensity.

    Parameters:
    - exp (oms.MSExperiment): The experiment containing the spectra.
    - precursor_mz (Optional[List[float]]): List of precursor m/z values to filter by.
    - retention_time (Optional[List[float]]): List of retention times to filter by.
    - rt_start (Optional[List[float]]): List of start retention times for filtering.
    - rt_end (Optional[List[float]]): List of end retention times for filtering.
    - precursor_mz_tolerance (float): Tolerance for precursor m/z filtering.
    - rt_tolerance (float): Tolerance for retention time filtering.
    - precursor_intensity_threshold (float): Minimum precursor intensity to include a spectrum.

    Returns:
    - List[oms.MSSpectrum]: Filtered list of spectra.
    """
    precursor_mz_tolerance *= 1e-6  # Convert tolerance to ppm

    # Validate input lists
    if precursor_mz is not None:
        if not isinstance(precursor_mz, list) or (retention_time is not None and not isinstance(retention_time, list)):
            raise ValueError("precursor_mz and retention_time must be lists")
        if len(precursor_mz) != len(retention_time):
            raise ValueError("precursor_mz and retention_time must be lists of equal length")

    def filter_condition(spectrum: oms.MSSpectrum, mz: float, rt_start: float, rt_end: float) -> bool:
        if not spectrum.getPrecursors():
            return False
        precursor = spectrum.getPrecursors()[0]
        mz_condition = abs(precursor.getMZ() - mz) < mz * precursor_mz_tolerance if mz is not None else True
        rt_condition = rt_start <= spectrum.getRT() <= rt_end if rt_start is not None and rt_end is not None else True
        return spectrum.getMSLevel() > 1 and precursor.getIntensity() > precursor_intensity_threshold and mz_condition and rt_condition

    combinations = []
    if precursor_mz is not None and rt_start is not None and rt_end is not None:
        combinations = zip(precursor_mz, rt_start, rt_end)
    elif precursor_mz is not None and retention_time is not None:
        combinations = zip(precursor_mz, retention_time, retention_time)  # Use retention_time for both start and end

    filtered_spectra = [s for s in exp for mz, start, end in combinations if filter_condition(s, mz, start, end)]
    # Remove duplicates based on NativeID
    unique_spectra = list({s.getNativeID(): s for s in filtered_spectra}.values())

    return unique_spectra

def ms2_to_mzml(spec, output_path):
    """
    Converts a list of MS2 spectra to an mzML file if the list is not empty.

    Parameters:
    - spec: A list of MS2 spectra.
    - output_path: The file path where the mzML file will be saved.
    """
    if spec:
        exp = oms.MSExperiment()
        exp.setSpectra(spec)
        oms.MzMLFile().store(output_path, exp)
    else:
        print("No spectra provided for conversion.")
        oms.MzMLFile().store(output_path, exp)

def pipeline(file_path: str, output_path: str, precmz: List[float], rt: List[float], RTstart: List[float], RTend: List[float], precmz_tolerance: float, rt_tolerance: float, precinty_thre: float, correct: bool = True, merge: bool = True) -> None:
    """
    Processes mass spectrometry data by correcting precursors, merging spectra, filtering MS2 spectra, and exporting to mzML format.

    Parameters:
    - file_path (str): Path to the input file.
    - output_path (str): Path for the output mzML file.
    - precmz (List[float]): List of precursor m/z values.
    - rt (List[float]): List of retention times.
    - RTstart (List[float]): List of start retention times.
    - RTend (List[float]): List of end retention times.
    - precmz_tolerance (float): Tolerance for precursor m/z filtering.
    - rt_tolerance (float): Tolerance for retention time filtering.
    - precinty_thre (float): Threshold for precursor intensity.
    - correct (bool): Whether to correct precursors.
    - merge (bool): Whether to merge spectra.
    """
    exp = load_experiment(file_path)
    if correct:
        correct_precursors(exp)
    if merge:
        merge_spectra(exp)
    filtered_ms2 = filter_ms2(exp, precmz=precmz, rt=rt, RTstart=RTstart, RTend=RTend, precmz_tolerance=precmz_tolerance, rt_tolerance=rt_tolerance, precinty_thre=precinty_thre)
    ms2_to_mzml(filtered_ms2, output_path)

def read_csv_to_df(file_path: str) -> Tuple[Optional[List[float]], Optional[List[float]], Optional[List[float]], Optional[List[float]]]:
    """
    Reads a CSV file and extracts columns for precursor m/z, retention time, start retention time, and end retention time.

    Parameters:
    - file_path (str): Path to the CSV file.

    Returns:
    - Tuple containing lists of precursor m/z, retention time, start retention time, and end retention time. None if the file path is empty or columns are missing.
    """
    if file_path:
        df = pd.read_csv(file_path)
        precmz = df['mz'].tolist() if 'mz' in df.columns else None
        rt = df['RT'].tolist() if 'RT' in df.columns else None
        RTstart = df['RTstart'].tolist() if 'RTstart' in df.columns else None
        RTend = df['RTend'].tolist() if 'RTend' in df.columns else None
        return precmz, rt, RTstart, RTend
    else:
        return None, None, None, None
