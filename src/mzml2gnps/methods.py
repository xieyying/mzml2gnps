import pandas as pd
import pyopenms as oms

def load_experiment(file_path):
    exp = oms.MSExperiment()
    oms.MzMLFile().load(file_path, exp)
    return exp

def correct_precursors(exp, mz_tolerance=0.5, ppm=False):
    delta_mzs, mzs, rts = [], [], []
    corr = oms.PrecursorCorrection()
    corr.correctToHighestIntensityMS1Peak(exp, mz_tolerance, ppm, delta_mzs, mzs, rts)

def merge_spectra(exp):
    mg = oms.SpectraMerger()
    mg.mergeSpectraPrecursors(exp)    

def filting_ms2(exp, precmz=None, rt=None, RTstart=None,RTend=None,precmz_tolerance=20, rt_tolerance=0.5, precinty_thre=0):
    precmz_tolerance *= 1e-6
    if precmz is not None and rt is not None:
        if not isinstance(precmz, list) or not isinstance(rt, list) or len(precmz) != len(rt):
            raise ValueError("precmz and rt must be lists of equal length")
    if precmz is not None and RTstart is not None and  RTend is not None:
        if not isinstance(precmz, list) or not isinstance(RTstart, list) or not isinstance(RTend, list) or len(precmz) != len(RTstart) or len(precmz) != len(RTend):
            raise ValueError("precmz and RTstart and RTend must be lists of equal length")

    def filter_condition1(spectrum, mz, r):
        if not spectrum.getPrecursors():
            return False
        prec = spectrum.getPrecursors()[0]
       
        mz_condition = abs(prec.getMZ() - float(mz)) < float(mz)*precmz_tolerance if mz is not None else True
        rt_condition = abs(spectrum.getRT() - r) < rt_tolerance if r is not None else True
        return spectrum.getMSLevel() > 1 and prec.getIntensity() > precinty_thre and mz_condition and rt_condition
    
    def filter_condition2(spectrum, mz, RTstart,RTend):
        if not spectrum.getPrecursors():
            return False
        prec = spectrum.getPrecursors()[0]
       
        mz_condition = abs(prec.getMZ() - float(mz)) < float(mz)*precmz_tolerance if mz is not None else True
        rt_condition = RTstart <= spectrum.getRT() <= RTend +3 if RTstart is not None and  RTend is not None else True
        return spectrum.getMSLevel() > 1 and prec.getIntensity() > precinty_thre and mz_condition and rt_condition
    

    if precmz is not None and RTstart is not None and  RTend is not None:
        combinations = list(zip(precmz, RTstart,RTend)) 
    elif precmz is not None and rt is not None:
        combinations = list(zip(precmz, rt))
    else:
        combinations = [(mz, r) for mz in (precmz if precmz is not None else [None]) for r in (rt if rt is not None else [None])]
         
    if precmz is not None and RTstart is not None and  RTend is not None:
        spectra = [s for s in exp for mz,rtstart,rtend in combinations if filter_condition2(s, mz,rtstart,rtend)]
        
    else:
        spectra = [s for s in exp for mz, r in combinations if filter_condition1(s, mz, r)]
        # Remove duplicate spectra
        spectra = list({s.getNativeID():s for s in spectra}.values())

    return  spectra 

def ms2_to_mzml(spec, output_path):
    """
    Store a list of MS2 spectra to an mzML file if the list is not empty.

    Parameters:
    - spec: A list of MS2 spectra.
    - output_path: The file path where the mzML file will be saved.
    """
    if spec:
        exp = oms.MSExperiment()
        exp.setSpectra(spec)
        oms.MzMLFile().store(output_path, exp)
    else:
        print("No spectra provided to store.")

def pipeline(file_path, output_path, precmz, rt, RTstart,RTend, precmz_tolerance, rt_tolerance, precinty_thre, correct=True, merge=True):
    exp = load_experiment(file_path)
    if correct:
        correct_precursors(exp)
    if merge:
        merge_spectra(exp)
    filtered_ms2 = filting_ms2(exp, precmz=precmz, rt=rt, RTstart=RTstart, RTend=RTend, precmz_tolerance=precmz_tolerance, rt_tolerance=rt_tolerance, precinty_thre=precinty_thre)
    if filtered_ms2:
        ms2_to_mzml(filtered_ms2, output_path)

def read_csv_to_df(file_path):
    if file_path:
        df = pd.read_csv(file_path)
        # Extract precmz and rt columns if they exist in the DataFrame
        precmz = df['mz'].tolist() if 'mz' in df.columns else None
        rt = df['RT'].tolist() if 'RT' in df.columns else None
        RTstart = df['RTstart'].tolist() if 'RTstart' in df.columns else None
        RTend = df['RTend'].tolist() if 'RTend' in df.columns else None
        return precmz, rt,RTstart,RTend
    else:
        return None, None,None,None
    
