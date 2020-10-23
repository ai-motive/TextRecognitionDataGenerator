#!/bin/bash
cd ..
ROOT_DIR=$(pwd)
export PYTHONPATH=${ROOT_DIR}
echo $PYTHONPATH

cd trdg
TRDG_DIR=${ROOT_DIR}/trdg
export PYTHONPATH=${PYTHONPATH}:${TRDG_DIR}
echo $PYTHONPATH

