#!/bin/bash

export RDMAV_FORK_SAFE=1
cd /data/rjfgroup/rjf01/cameron.parker/builds/Bayes-Tune
python3.8 -m IPython -c "run $1"