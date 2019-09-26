#!/usr/bin/python
#################################################
# Purpose: Run ISCE2StaMPS and StaMPS processing
# Author: Alexander Torres
# Updated: September 19, 2019
#################################################

import os
import subprocess
import json
import logging
from datetime import datetime

# logging setup
log_format = "[%(asctime)s: %(levelname)s/%(funcName)s] %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)

# load _context.json if it exists
ctx = {}
ctx_file = "_context.json"
if os.path.exists(ctx_file):
    with open(ctx_file) as f:
        ctx = json.load(f)
logging.info("ctx: {}".format(json.dumps(ctx, indent=2)))


#################################################
# Create ISCE2StaMPS input_file
#################################################
# get parameters for ISCE2StaMPS "input_file"
# fixed input
source_data = "slc_stack"
slc_suffix = ".full"
geom_suffix = ".full"

# dynmaic input
if os.path.exists("merged") is True:
    # get absolute path for SLC, geom_master, and baselines directory
    slc_stack_path = os.path.abspath("merged/SLC")
    slc_stack_geom_path = os.path.abspath("merged/geom_master")
    slc_stack_baseline_path = os.path.abspath("merged/baselines")
    maskfile = os.path.abspath("merged/geom_master/shadowMask.rdr.full")
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
wavelength= ctx.get("wavelength")

# Create "input_file"
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


#################################################
# Run make_single_master_stack_isce, mt_prep_isce, and stamps
#################################################
# get parameters for mt_prep_isce
amplitude_dispersion=ctx.get("amplitude_dispersion")
number_patches_range=ctx.get("number_patches_range")
number_patches_azimuth=ctx.get("number_patches_azimuth")
overlapping_pixels_range=ctx.get("overlapping_pixels_range")
overlapping_pixels_azimuth = ctx.get("overlapping_pixels_azimuth")
insar_dir = "INSAR_{}".format(slc_stack_master)

make_master_stack = subprocess.Popen(["make_single_master_stack_isce"],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

cd_insar_dir = subprocess.Popen(["cd", insar_dir],
                      stdin=make_master_stack.stdout,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)

mt_prep_isce = subprocess.Popen(["mt_prep_isce",
                                 amplitude_dispersion,
                                 number_patches_range,
                                 number_patches_azimuth,
                                 overlapping_pixels_range,
                                 overlapping_pixels_azimuth],
                                stdin=cd_insar_dir.stdout,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

stamps = subprocess.Popen(["stamps"],
                      stdin=mt_prep_isce.stdout,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)

output, error = stamps.communicate()

# Print output and error to log
logging.info(output)
logging.info(error)



