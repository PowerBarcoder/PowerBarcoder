#!/bin/bash

## Maximum number of CPU cores
#MAX_CPU=36
#
#for ((CPU_COUNT = 2; CPU_COUNT <= MAX_CPU; CPU_COUNT += 2)); do
#  # Run the Docker container with the specified number of CPU cores
#  docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder_$CPU_COUNT --cpus=$CPU_COUNT powerbarcoder
#done

# Run the Docker container with the specified number of CPU cores
docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder_2 --cpus=2 powerbarcoder
docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder_4 --cpus=4 powerbarcoder
docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder_8 --cpus=8 powerbarcoder
docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder_16 --cpus=16 powerbarcoder
docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder_24 --cpus=24 powerbarcoder
docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder_32 --cpus=32 powerbarcoder

#This might not be necessary
docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder_36 --cpus=36 powerbarcoder
