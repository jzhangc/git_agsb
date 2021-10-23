# AGSB

"A good shopping bot" is purely for educational purposes. DO NOT use this to buy things online.

## Instructions (Oct.2021)

The program is based on selenium. See [here](https://pypi.org/project/selenium/) for details.

NOTE: The following contains steps to install on Intel Mac running macOS 11.

1. System requirement

    Anything Mac or Linux systems with an internet connection.

2. Install miniforge3 (mini coda with forge channel as default)

   url: <https://github.com/conda-forge/miniforge#miniforge3>

        bash Miniforge3-MacOSX-arm64.sh

   NOTE 1: Although it is possible to use `conda config --add channels conda-forge`  to manually add the `forge` channel to miniconda, it is generally recommended using miniforge version of conda for both Apple and Intel chips.

3. Create, setup and activate a conda environment

        conda env create -f ./inst/environment_agsb.yml --prefix ./conda_venv_agsb
        conda activate ./conda_venv_tf_metal

4. Known issues

    TBD
