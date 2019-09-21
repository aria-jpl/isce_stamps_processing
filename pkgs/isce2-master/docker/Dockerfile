FROM hysds/pge-base:latest

# Set an encoding to make things work smoothly.
ENV LANG en_US.UTF-8

# Set ISCE repo
ENV ISCE_ORG isce-framework

# set to root user
USER root

# install tools for RPM generation
RUN set -ex \
 && yum update -y \
 && yum groupinstall -y "development tools" \
 && yum install -y \
      make ruby-devel rpm-build rubygems \
 && gem install --no-ri --no-rdoc fpm

# install isce requirements
RUN set -ex \
 && . /opt/conda/bin/activate root \
 && conda install --yes \
      cython \
      gdal \
      git \
      h5py \
      libgdal \
      pytest \
      numpy \
      fftw \
      scipy \
      basemap \
      scons \
      opencv \
      hdf4 \
      hdf5 \
      netcdf4 \
      libgcc \
      libstdcxx-ng \
      cmake \
 && yum install -y uuid-devel x11-devel motif-devel jq \
 && ln -sf /opt/conda/bin/cython /opt/conda/bin/cython3

# link system libuuid
RUN set -ex \
 && cd /opt/conda/lib \
 && unlink libuuid.so \
 && unlink libuuid.so.1 \
 && ln -s /lib64/libuuid.so.1.3.0 libuuid.so \
 && ln -s /lib64/libuuid.so.1.3.0 libuuid.so.1

# install libgfortran.so.3 and create missing link
RUN set -ex \
 && yum install -y gcc-gfortran \
 && cd /lib64 \
 && ( test -f libgfortran.so || ln -sv libgfortran.so.*.* libgfortran.so )

# copy repo
COPY . /root/isce2

# build ISCE
RUN set -ex \
 && . /opt/conda/bin/activate root \
 && cd /root \
 && source isce2/docker/build_env.sh \
 && mkdir -p $BUILD_DIR \
 && cp isce2/docker/SConfigISCE isce2/configuration/ \
 && cd isce2 \
 && scons install \
 && cp docker/isce_env.sh $ISCE_INSTALL_ROOT \
 && mkdir -p rpm-build/opt \
 && mv $ISCE_INSTALL_ROOT rpm-build/opt \
 && curl -s https://api.github.com/repos/$ISCE_ORG/isce2/git/refs/heads/master \
    > rpm-build/opt/isce2/version.json \
 && hash=$(cat rpm-build/opt/isce2/version.json | jq -r .object.sha) \
 && short_hash=$(echo $hash | cut -c1-5) \
 && fpm -s dir -t rpm -C rpm-build --name isce \
      --prefix=/ --version=2.0 --provides=isce \
      --maintainer=piyush.agram@jpl.nasa.gov \
      --description="InSAR Scientific Computing Environment v2 (${hash})"

FROM hysds/pge-base:latest

# Set an encoding to make things work smoothly.
ENV LANG en_US.UTF-8

# install ISCE from RPM
COPY --from=0 /root/isce2/isce-2.0-1.x86_64.rpm /tmp/isce-2.0-1.x86_64.rpm

# install isce and its minimal requirements
RUN set -ex \
 && sudo /opt/conda/bin/conda install --yes \
      gdal \
      h5py \
      libgdal \
      pytest \
      numpy \
      fftw \
      scipy \
      basemap \
      opencv \
      hdf4 \
      hdf5 \
      netcdf4 \
 && sudo yum update -y \
 && sudo yum install -y uuid-devel x11-devel motif-devel gcc-gfortran \
 && cd /opt/conda/lib \
 && sudo unlink libuuid.so \
 && sudo unlink libuuid.so.1 \
 && sudo ln -s /lib64/libuuid.so.1.3.0 libuuid.so \
 && sudo ln -s /lib64/libuuid.so.1.3.0 libuuid.so.1 \
 && cd /lib64 \
 && ( test -f libgfortran.so || sudo ln -sv libgfortran.so.*.* libgfortran.so ) \
 && sudo yum install -y /tmp/isce-2.0-1.x86_64.rpm \
 && sudo yum clean all \
 && sudo rm -rf /var/cache/yum \
 && sudo rm /tmp/isce-2.0-1.x86_64.rpm
