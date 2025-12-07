#!/usr/bin/bash
# setup script for the project

# vars
VENV_PATH=".venv"
PYPROJECT_FILE="requirements.txt"
ACTIAVTE_BASH="$VENV_PATH/bin/activate"

# package install function
install_modules() {
    # checking to see if pyproject exists
    if [[ -f "$PYPROJECT_FILE" ]]; then
        echo "pyproject exists, installing packages now"
        pip install -r $PYPROJECT_FILE
    else
        echo "pyproject doesn't exist, please create one or download from the repo"
        exit
    fi

}

# checking to see if it exists before we create a new one
if [[ -d "$VENV_PATH" ]]; then
    echo "venv exists, moving on to installing packages"
    source $ACTIAVTE_BASH
    install_modules
else
    echo "venv does not exist, creating one now."
    python3 -m venv .venv
    echo "installing packages..."
    source "$ACTIAVTE_BASH"
    install_modules
fi