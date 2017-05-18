#!/bin/bash

BASEBALL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EMULATOR_PYTHON_PATH=$BASEBALL_DIR"/emulator/scoreboard_emulator.py"
PYTHON=`which python`

$PYTHON $EMULATOR_PYTHON_PATH "${@}"
