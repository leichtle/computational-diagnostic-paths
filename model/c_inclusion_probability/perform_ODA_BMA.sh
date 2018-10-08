#!/bin/sh

export PATH=/software/bin:$PATH

R CMD BATCH ./perform_ODA_BMA.r
