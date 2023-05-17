FROM ghcr.io/osgeo/gdal:ubuntu-full-3.6.4

ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

RUN apt-get update && \
    apt-get install -y \
      build-essential \
      fish \
      git \
      wget \
      python3-pip \
      # For Psycopg2
      libpq-dev python3-dev \
      # NetCDF stuff
      libhdf5-serial-dev netcdf-bin libnetcdf-dev \
      # Shouldn't need this
      # libgeos-dev \
    && apt-get autoclean && \
    apt-get autoremove && \
    rm -rf /var/lib/{apt,dpkg,cache,log}

RUN mkdir -p /conf
# Run pip-compile --resolver=backtracking --output-file requirements.txt requirements.in
# to update the requirements.txt
COPY requirements.txt /conf/
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /conf/requirements.txt

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

WORKDIR /code

CMD ["jupyter", "notebook", "--allow-root", "--ip='0.0.0.0'", "--port=8888"]
