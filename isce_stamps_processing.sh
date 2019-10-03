#!/bin/bash

# copy packages from isce_stamps_processing repo 
cp -rf $HOME/isce_stamps_processing/pkgs/* $HOME/verdi/pkgs/

# source paths for StaMPS processing
source $HOME/isce_stamps_processing/pkgs/StaMPS-master/StaMPS_CONFIG.bash

if [[ -e $TRIANGLE_BIN/triangle ]]
then
    echo Triangle Bin Exists!
else
    cd $HOME/verdi/pkgs/triangle
    make
    mkdir bin
    cp triangle bin/
fi

if [[ -e $SNAPHU_BIN/snaphu ]]
then
    echo Snaphu Bin Exists!
else
    cd $HOME/verdi/pkgs/snaphu-v2.0.0/src
    make
fi

# run StaMPS processing
python $HOME/isce_stamps_processing/isce_stamps_processing.py
