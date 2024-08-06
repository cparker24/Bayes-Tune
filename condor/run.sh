#!/bin/bash

export RDMAV_FORK_SAFE=1
python3.8 -m IPython -c "run $1"