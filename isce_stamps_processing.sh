#!/bin/bash

# copy packages from isce_stamps_processing repo 
sudo cp -rf $HOME/isce_stamps_processing/pkgs/ $HOME/verdi/pkgs/

# source paths for StaMPS processing
source $HOME/isce_stamps_processing/pkgs/StaMPS-master/StaMPS_CONFIG.bash 

if ![ -f "$TRIANGLE_BIN/triangle" ]; then
	cd $HOME/verdi/pkgs/triangle/src
	make
	cp triangle bin/
fi

if ![ -f "$SNAPHU_BIN/snaphu" ]; then
	cd $HOME/verdi/pkgs/snaphu-v2.0.0/src
	make
fi

# run StaMPS processing
python $HOME/isce_stamps_processing/isce_stamps_processing.py