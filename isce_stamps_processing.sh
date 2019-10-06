#!/bin/bash
#################################################
# Purpose: Run StaMPS processing PGE
# Author: Alexander Torres
# Updated: October 6, 2019
#################################################

# start anaconda
eval "$(/home/ops/miniconda/bin/conda shell.bash hook)"

# save work directory
WORK_DIR=$(pwd)

# copy packages from isce_stamps_processing repo 
if [[ -e $HOME/verdi/pkgs ]]
then
    cp -rf $HOME/isce_stamps_processing/pkgs/* $HOME/verdi/pkgs/
else
    mkdir $HOME/verdi/pkgs
    cp -rf $HOME/isce_stamps_processing/pkgs/* $HOME/verdi/pkgs/
fi

# source paths for StaMPS processing
. $HOME/isce_stamps_processing/pkgs/StaMPS-master/StaMPS_CONFIG.bash

# check for Triangle executable
if [[ -e $TRIANGLE_BIN/triangle ]]
then
    echo Triangle Bin Exists!
else
    cd $HOME/verdi/pkgs/triangle
    make
    mkdir bin
    cp triangle bin/
    cd $WORK_DIR
fi

# check for SNAPHU executable 
if [[ -e $SNAPHU_BIN/snaphu ]]
then
    echo Snaphu Bin Exists!
else
    cd $HOME/verdi/pkgs/snaphu-v2.0.0/src
    make
    cd $WORK_DIR
fi

# run StaMPS processing
python $HOME/isce_stamps_processing/isce_stamps_processing.py
