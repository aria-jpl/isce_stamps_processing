#!/usr/bin/python
#################################################
# Purpose: Run ISCE2StaMPS and StaMPS processing
# Author: Alexander Torres
# Updated: October 6, 2019
#################################################

import os
import subprocess
import json
import logging
import stat
from  multiprocessing import cpu_count
from datetime import datetime

# get work directory
cwd = os.getcwd()

# logging setup
log_format = "[%(asctime)s: %(levelname)s/%(funcName)s] %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)

# load _context.json if it exists
ctx = {}
ctx_file = "_context.json"
if os.path.exists(ctx_file):
    with open(ctx_file) as f:
        ctx = json.load(f)
#logging.info("ctx: {}".format(json.dumps(ctx, indent=2)))


#################################################
# Create ISCE2StaMPS input_file
#################################################
# get parameters for ISCE2StaMPS "input_file"
# fixed input
source_data = "slc_stack"
slc_suffix = ".full"
geom_suffix = ".full"

# get SLC stack directory
for (root, dirs, filenames) in os.walk(cwd):
    print("cwd: {}".format(cwd))
    print("dirs {}".format(dirs))
    if (dirs[0].find("coregistered_slcs") == 0):
        break
coreg_full_path = os.path.join(root, dirs[0])
merged_full_path = os.path.join(root, dirs[0], "merged")
print("merged_full_path: {}".format(merged_full_path))

# dynmaic input
if os.path.exists(merged_full_path) is True:
    # get absolute path for SLC, geom_master, and baselines directory
    slc_stack_path = os.path.join(merged_full_path,"SLC")
    slc_stack_geom_path = os.path.join(merged_full_path,"geom_master")
    slc_stack_baseline_path = os.path.join(merged_full_path,"baselines")
    maskfile = os.path.join(merged_full_path,"geom_master/shadowMask.rdr.full")
    # get slc stack master date
    slc_dates = os.listdir(slc_stack_path)
    slc_dates.sort(key=lambda date: datetime.strptime(date,'%Y%m%d'))
    slc_stack_master = slc_dates[0]
else:
    raise Exception("ERROR: Cannot find merged directory in work directory")

# user input
range_looks = ctx.get("range_looks")
azimuth_looks = ctx.get("azimuth_looks")
aspect_ratio = ctx.get("aspect_ratio")
wavelength = ctx.get("lambda")

# create "input_file"
with open("input_file", "w+") as input_file:
    input_file.write("source_data {}\n".format(source_data))
    input_file.write("slc_stack_path {}\n".format(slc_stack_path))
    input_file.write("slc_stack_master {}\n".format(slc_stack_master))
    input_file.write("slc_stack_geom_path {}\n".format(slc_stack_geom_path))
    input_file.write("slc_stack_baseline_path {}\n".format(slc_stack_baseline_path))
    input_file.write("range_looks {}\n".format(range_looks))
    input_file.write("aspect_ratio {}\n".format(aspect_ratio))
    input_file.write("azimuth_looks {}\n".format(azimuth_looks))
    input_file.write("lambda {}\n".format(wavelength))
    input_file.write("slc_suffix {}\n".format(slc_suffix))
    input_file.write("geom_suffix {}\n".format(geom_suffix))
    input_file.write("maskfile {}".format(maskfile))
input_file.close()


##############################################################
# Run make_single_master_stack_isce, mt_prep_isce, and stamps
##############################################################
# get parameters for mt_prep_isce
amplitude_dispersion=str(ctx.get("amplitude_dispersion"))
number_patches_range=str(int(ctx.get("number_patches_range")))
number_patches_azimuth=str(int(ctx.get("number_patches_azimuth")))
overlapping_pixels_range=str(int(ctx.get("overlapping_pixels_range")))
overlapping_pixels_azimuth=str(int(ctx.get("overlapping_pixels_azimuth")))
insar_dir = "INSAR_{}".format(slc_stack_master)
insar_full_path = os.path.join(root, insar_dir)


# run make_single_master_stack_isce
cp = subprocess.run(["make_single_master_stack_isce"], check=True)

# change to INSAR directory
try:
    os.chdir(insar_dir)
except FileNotFoundError as e:
    print(e)

# run mt_prep_isce
cp = subprocess.run(["mt_prep_isce", amplitude_dispersion, number_patches_range, number_patches_azimuth, overlapping_pixels_range, overlapping_pixels_azimuth], check=True)

# set number of cores of machine
cores = str(cpu_count())
cp = subprocess.run(["/home/ops/isce_stamps_processing/setparm_app_linux/setparm", 'n_cores', cores], check=True)

# run stamps MATLAB standalone application
cp = subprocess.run(["/home/ops/isce_stamps_processing/stamps_app_linux/stamps"], check=True)

if cp.returncode == 0:
    # rm coregistered slc context.json, dataset.json, and met.json 
    os.remove(os.chmod(os.path.join(coreg_full_path, "*context.json"), stat.S_IWRITE))
    os.remove(os.chmod(os.path.join(coreg_full_path, "*dataset.json"), stat.S_IWRITE))
    os.remove(os.chmod(os.path.join(coreg_full_path, "*met.json"), stat.S_IWRITE))
