# Purpose: This bash script was modified for hysds-pge use
# Author: Alexander Torres

#####################################
# StaMPS 
#####################################
export STAMPS="/home/ops/verdi/pkgs/StaMPS-master" 
export SAR="/home/ops/verdi/pkgs/isce2-master" 
export TRIANGLE_BIN="/home/ops/verdi/pkgs/triangle/bin" 
export SNAPHU_BIN="/home/ops/verdi/pkgs/snaphu-v2.0.0/bin"
#export GETORB_BIN="/home/ahooper/software/getorb/bin"
#export SAR_ODR_DIR="/home/ahooper/software/SAR_FILES/ODR"
#export SAR_PRC_DIR  "/home/ahooper/software/SAR_FILES/PRC"
#export VOR_DIR="/home/ahooper/software/SAR_FILES/VOR"
#export INS_DIR="/home/ahooper/software/SAR_FILES/INS"
#export DORIS_BIN="/home/ahooper/software/doris_v4.02/bin"
#####################################


#####################################
# ISCE 2
#####################################
export ISCE_CONTRIB_BIN=/home/ops/verdi/pkgs/isce2-master/contrib/timeseries/prepStackToStaMPS/bin
export ISCE_APP=/home/ops/verdi/pkgs/isce2-master/applications
#####################################


#####################################
# ROI_PAC VERSION 3 
#####################################
export ROI_PAC="$SAR/ROI_PAC"
export INT_BIN="$ROI_PAC/INT_BIN"
export INT_SCR="$ROI_PAC/INT_SCR"
#####################################


#####################################
# ROI_PAC VERSION 2.3 and before 
#####################################
#set MACH=`uname -s`
#if ($MACH == "HP-UX") then
#  export ARCHC=HP
#else if ($MACH == "IRIX") then
#  export ARCHC=SGI
#else if ($MACH == "SunOS") then
#  export ARCHC=SUN
#else if ($MACH == "Linux") then
#  export ARCHC=LIN
#else if ($MACH == "Darwin") then
#  export ARCHC=MAC
#fi
#export INT_LIB="$ROI_PAC/LIB/$ARCHC"
#export INT_BIN="$ROI_PAC/BIN/$ARCHC"
#export FFTW_LIB="$SAR/FFTW/$ARCHC""_fftw_lib"
#####################################


#####################################
# shouldn't need to change below here
#####################################

export MY_BIN="$INT_BIN"
export MATLABPATH=$STAMPS/matlab`echo $MATLABPATH`
export DORIS_SCR="$STAMPS/DORIS_SCR"

# Needed for ROI_PAC (a bit different to standard)

### use points not commas for decimals, and give dates in US english
export LC_NUMERIC="en_US.UTF-8"
export LC_TIME="en_US.UTF-8"


export MY_SAR="$SAR"
export OUR_SCR="$MY_SAR/OUR_SCR"
export MY_SCR="$STAMPS/ROI_PAC_SCR"

export SAR_TAPE="/dev/rmt/0mn"

export PATH=${PATH}:$STAMPS/bin:$MY_SCR:$INT_BIN:$INT_SCR:$OUR_SCR:$DORIS_SCR:$GETORB_BIN:$DORIS_BIN:$TRIANGLE_BIN:$SNAPHU_BIN:$ISCE_CONTRIB_BIN:$ISCE_APP:$MATLABPATH



