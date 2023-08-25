#!/bin/sh

sphinx-apidoc --force -o . ../src 
make clean html
make html
docker build . -t gadgetronimages.azurecr.io/mrftools-docs:v0.0.3
docker push gadgetronimages.azurecr.io/mrftools-docs:v0.0.3