# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 13:44:34 2014

Takes multiple scenes from an "INPUT" (input_dir) directory and produces 
Seperate extracted outputs in an "OUTPUT" (output_path) directory.

!! OUTPUT CANT BE A SUBDIRECTORY OF INPUT !!

@author: SHAUNAK
"""

import os.path
import subprocess

# Read all the files in a given folder
input_dir = "F:\\Work_IITB\\multidate\\" #Working Directory
program_root = "C:\\Program Files (x86)\\PolSARpro_v4.2.0\\" #PolSAR installation
output_dir = "F:\\Work_IITB\\output"

# Make sure that the output directory exists
if ( os.path.isdir(output_dir) == False ):
    os.mkdir(output_dir)

# Soft/data_import/airsar_header.exe
# Arguments: 
# "E:/Data/UAVSAR/Haywrd_multiangle/Haywrd_05501_10080_007_101110_L090_CX_01.dat" 
# "C:/Users/SHAUNAK/AppData/Local/Temp/PolSARpro_4.2.0/Tmp/2014_10_06_12_05_59_airsar_config.txt" 
# "C:/Users/SHAUNAK/AppData/Local/Temp/PolSARpro_4.2.0/Tmp/2014_10_06_12_05_59_airsar_fst_header_config.txt" 
# "C:/Users/SHAUNAK/AppData/Local/Temp/PolSARpro_4.2.0/Tmp/2014_10_06_12_05_59_airsar_par_header_config.txt" 
# "C:/Users/SHAUNAK/AppData/Local/Temp/PolSARpro_4.2.0/Tmp/2014_10_06_12_05_59_airsar_cal_header_config.txt" 
# "C:/Users/SHAUNAK/AppData/Local/Temp/PolSARpro_4.2.0/Tmp/2014_10_06_12_05_59_airsar_dem_header_config.txt"
# old MLC


for root, dirs, files in  os.walk(input_dir):
    #pick up each file and run the extraction steps
    for file in files:
        ## first gather metadata
        program_path = os.path.join(program_root, "Soft\\data_import\\airsar_header.exe")
        scene_name = file.split(".")[0] 
        scene_path = os.path.join(output_dir,scene_name)
        print(scene_name) # Print the current file under consideration 
        # Make a new directory for each scene
        if ( os.path.isdir(os.path.join(output_dir,scene_name)) == False ):
            os.mkdir(os.path.join(output_dir,scene_name))
        # Extract the metadata
        subprocess.call([program_path, os.path.join(root,file), 
                         os.path.join(scene_path,scene_name)+"_config.txt",
                         os.path.join(scene_path,scene_name)+"_fst.txt",
                         os.path.join(scene_path,scene_name)+"_par.txt",
                         os.path.join(scene_path,scene_name)+"_cal.txt",
                         os.path.join(scene_path,scene_name)+"_dem.txt","old","MLC"], shell=True) 
                         
        # Read the files to figure out the parameters for the second call!
        config_file_f = open(os.path.join(scene_path,scene_name)+"_config.txt")
        configuration = config_file_f.readlines()
        config_file_f.close()
        
        num_lines = int(configuration[2].split()[0])
        num_cols = int(configuration[5].split()[0])
                         
        # Process The Function Soft/data_import/airsar_convert_T3.exe
        # Arguments: "E:/Data/UAVSAR/Haywrd_multiangle/Haywrd_05501_10080_007_101110_L090_CX_01.dat" "E:/Data/UAVSAR/Haywrd_multiangle/T3" 3300 0 0 18672 3300 "C:/Users/SHAUNAK/AppData/Local/Temp/PolSARpro_4.2.0/Tmp/2014_10_06_12_05_59_airsar_config.txt" 1 1
        #  airsar_convert_T3 stk_file_name out_dir Ncol offset_lig offset_col sub_nlig sub_ncol HeaderFile SubSampRG SubSampAZ 
        
        #Update the program path
        program_path = os.path.join(program_root, "Soft\\data_import\\airsar_convert_T3.exe")
        
        #CHECK / Make the T3 directory
        T3_Path = os.path.join(os.path.join(scene_path,"T3"))
        if( os.path.isdir(T3_Path) == False):
            os.mkdir(T3_Path)
            
        mlAz = "1"
        mlRg = "1"
        subprocess.call([program_path, 
                         os.path.join(root,file), T3_Path, 
                        str(num_cols), "0", "0", str(num_lines), str(num_cols), os.path.join(scene_path,scene_name)+"_config.txt", mlAz, mlRg])
                        
        #Make the pauli RGB
        program_path = os.path.join(program_root, "Soft\\bmp_process\\create_pauli_rgb_file_T3.exe")
        subprocess.call([program_path, 
                         T3_Path, os.path.join(T3_Path,"PauliRGB.BMP"), str(num_cols),
                        "0", "0", str(num_lines), str(num_cols)])
                        