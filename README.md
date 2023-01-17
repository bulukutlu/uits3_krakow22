# Analysis Software for the Krakow22 test beam
Tools and software for the analysis of test beam data recorded in the Krakow Bronowice Cyclotron in November 2022 using uITS3+Califa setup.

## Useful links

1. Getting started with ITS3 WP3 test beam analysis

    https://twiki.cern.ch/twiki/bin/viewauth/ALICE/GettingStartedWithTestbeamAnalysis
2. Corryvreckan manual

    https://gitlab.cern.ch/corryvreckan/corryvreckan/-/jobs/artifacts/master/raw/public/usermanual/corryvreckan-manual.pdf?job=cmp%3Ausermanual
3. ITS3 Corryvreckan tools GitLab

    https://gitlab.cern.ch/alice-its3-wp3/its-corryvreckan-tools


# Requirements
> Following installation steps were tested in Ubuntu 22.04.1 LTS and works
## ROOT
ROOT is a data analysis framework developed by CERN, the European Organization for Nuclear Research. It is a C++ based framework that provides a set of tools for storing, processing, and analyzing large amounts of data.

Before installing ROOT make sure to get the required dependencies:
```
sudo apt update
sudo apt upgrade

sudo apt-get install dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev libxft-dev libxext-dev python libssl-dev
```

To install ROOT on your system, you can follow these steps:

1. First, download a version of ROOT from the official website (https://root.cern/downloading-root). You can choose to download the source code or a pre-compiled binary package, depending on your preference and system configuration. Here I tested with `6.24.6` and it works so you can just do:
    ```
    mkdir root && cd root
    wget https://root.cern/download/root_v6.24.06.source.tar.gz
    ```

2. Extract the downloaded package:
    ```
    tar -zxvf root_v6.24.06.source.tar.gz
    mkdir build-root6.24.06 && cd build-root6.24.06/
    ```

3. Use CMake and build/install the extracted package:
    ```
    cmake -DCMAKE_CXX_STANDARD=17 -Dgdml=ON -Dmathmore=ON -Dthread=ON -Dpython3=ON -Dminuit2=ON -Dgenvector=ON ../root-6.24.06
    make -j$(nproc)
    make install
    ```

4. Once the installation is complete, you can test the installation by running the ROOT interpreter:
    ```
    root
    ```
This should open the ROOT command prompt, where you can enter ROOT commands and interact with the framework.

Note that the installation process may vary depending on your system configuration and the version of ROOT you are installing. If you encounter any issues during the installation, you can refer to the ROOT documentation or seek help on the ROOT forum (https://root-forum.cern.ch/).

## EUDAQ2
EUDAQ2 (European Data Acquisition System) is a software package developed by the CMS Experiment at CERN for data acquisition and data transfer in high-energy physics experiments. 

To install EUDAQ2 on your system, you can follow the instructions provided in the EUDAQ2 documentation (https://eudaq.web.cern.ch/eudaq/documentation/). The documentation provides detailed instructions on how to download and install EUDAQ2, as well as how to use it for data acquisition and data processing in particle physics experiments.

Here are suggested installation steps (requires CERN account & being in the ITS3-WP3 mailing list):
```
git clone https://gitlab.cern.ch/alice-its3-wp3/eudaq2.git
cd eudaq2
mkdir build && cd build
cmake -DEUDAQ_BUILD_PYTHON=ON  -DUSER_ITS3_BUILD=ON -DCMAKE_CXX_STANDARD=17 ..
make -j$(nproc)
make install
```

## Corryvreckan
Corryvreckan is a software framework used for analyzing data from particle physics experiments, particularly those conducted at CERN's Large Hadron Collider. It is written in C++ and offers tools for processing and visualizing data, as well as a graphical user interface. Corryvreckan is typically used in conjunction with other software packages such as ROOT and EUDAQ. To install it, you can follow the instructions provided in the Corryvreckan documentation (https://corryvreckan.readthedocs.io/en/latest/installation.html). But here we want to keep up-to-date with ITS3 developments so use the following instructions (requires CERN account):

```
git clone https://gitlab.cern.ch/alice-its3-wp3/corryvreckan.git
cd corryvreckan
mkdir build && cd build
```
Don't forget to give the path to the EUDAQ2 installation:
```
cmake -DBUILD_EventLoaderEUDAQ=OFF -DBUILD_EventLoaderATLASpix=OFF -DBUILD_EventLoaderCLICpix=OFF -DBUILD_EventLoaderCLICpix2=OFF -DBUILD_EventLoaderMuPixTelescope=OFF -DBUILD_EventLoaderTimepix1=OFF -DBUILD_EventLoaderTimepix3=OFF -DCMAKE_INSTALL_PREFIX=../ -DBUILD_EventLoaderEUDAQ2=ON -Deudaq_DIR=add_here_eudaq2_path/cmake ..
```
```
make -j$(nproc)
make install
```
Check installation:
```
corry --help
```
> ### Note: 
> For accessing the corry objects in ROOT you need to add the shared library to the gSystem.
> 
> For example when you enter ROOT:
> ```
>  gSystem->Load("/home/berki/Software/corryvreckan/lib/libCorryvreckanObjects.so")
> ```
>  Or in macros:
> ```
>  gSystem->AddLinkedLibs("-L /home/berki/Software/corryvreckan/lib -l libCorryvreckanObjects.so");
> ```
>To-Do: Need to check if there is not another way. 
