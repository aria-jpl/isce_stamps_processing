FROM hysds/pge-base:latest
MAINTAINER Alexander P Torres "alexander.p.torres@jpl.nasa.gov"

ARG id
ARG gid

# copy isce_stamps_processing code
COPY . /home/ops/isce_stamps_processing
ENV ISCE_STAMPS_PROCESSING=/home/ops/isce_stamps_processing

# Setup MATLAB Runtime, isce_stamps_processing github repo, and Miniconda 3
RUN sudo yum update -y \
 && sudo yum install wget unzip libXext libXt-devel libXmu tcsh -y \
 && sudo yum groupinstall 'Development Tools' -y \
 && mkdir mcr-install \
 && cd mcr-install \
 && wget https://ssd.mathworks.com/supportfiles/downloads/R2019a/Release/5/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2019a_Update_5_glnxa64.zip \
 && unzip MATLAB_Runtime_R2019a_Update_5_glnxa64.zip \
 && sudo ./install -mode silent -agreeToLicense yes \
 && cd .. \
 && rm -Rf mcr-install \
 && mkdir tmp \
 && cd tmp \
 && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
 && bash ~/miniconda.sh -b -p $HOME/miniconda \
 && sudo chown -R ops /opt/conda \
 && eval "$(/home/ops/miniconda/bin/conda shell.bash hook)" \
 && conda install -y -c conda-forge isce2 \
 && conda install -y -c anaconda mesa-libgl-cos6-x86_64
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/MATLAB/MATLAB_Runtime/v96/runtime/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v96/bin/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v96/sys/os/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/v96/extern/bin/glnxa64
ENV XAPPLRESDIR=/usr/local/MATLAB/MATLAB_Runtime/v901/X11/app-defaults
ENV MCR_CACHE_VERBOSE=true
ENV MCR_CACHE_ROOT=/tmp

# Set entrypoint
USER ops
WORKDIR /home/ops
CMD ["/bin/bash", "--login"]
