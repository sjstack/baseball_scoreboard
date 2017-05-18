
BASEBALL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EMULATOR_PYTHON_PATH=$BASEBALL_DIR"/emulator/scoreboard_emulator.py"
PYTHON=`which python`

echo $EMULATOR_PYTHON_PATH
echo $PYTHON

$PYTHON $EMULATOR_PYTHON_PATH "${@}"
