from pyopenms import DIAUmpire
from pyopenms import MSExperiment, MzMLFile

def dia_umpire_recon(input_mzML, output_mzML): #TODO
    """
    使用DIA-Umpire重建伪DDA谱图
    """ 
    dia = DIAUmpire()
    dia_params = dia.getDefaults()
    dia_params.setValue("mz_tolerance", 0.05)  # m/z 容差（单位：Da）
    dia.setParameters(dia_params)
    
    # 运行重建
    recon_exp = MSExperiment()
    dia.reconstruct(input_mzML, recon_exp)
    
    # 保存伪谱图
    MzMLFile().store(output_mzML, recon_exp)
    print(f"伪DDA谱图已保存至 {output_mzML}")

if __name__ == "__main__":
    input = r'D:\workissues\manuscript\halo_mining\HaloAnalyzer\MSE_data\250325_StandardCompounds_MSE_Continuum_6ul1.mzML'
    output = r'D:\workissues\manuscript\halo_mining\HaloAnalyzer\MSE_data\recon_DDA.mzML'
    dia_umpire_recon(input, output)
    # dia_umpire_recon("MSE_data.mzML", "recon_DDA.mzML")

