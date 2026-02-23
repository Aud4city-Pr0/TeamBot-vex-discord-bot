# powershell setupscript

# vars
$VENV_PATH=".venv"
$PYPROJECT_FILE="pyproject.toml"

# functions
functions Install-Packages() {
    if(Test-Path -Path $PYPROJECT_FILE) {
        Write-Host "pyproject exists, installing packages now"
        python3 -m pip install -r $PYPROJECT_FILE
    } else {
        Write-Host "pyproject doesn't exist, please create one or download from the repo and re-run the script"
        exit
    }
}

# checking to see if .venv is real
if(Test-Path -Path $VENV_PATH) {
    Write-Host ".venv exists, installing packages now"
} else {
    Write-Host ".venv doesn't, creating one now"
    python -m venv venv
    Write-Host "installing packages now..."

}