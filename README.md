# data-evaluator
This repo is dedicated to evaluate the data gathered in https://github.com/dtrosien/data-collector


# Developer setup
## Python setup
Install anaconda.<br/>
Create an anaconda environment `conda create -n data-evaluator python=3.11` so the packages will be encapsulated for this project and do not interfere with other Python projects.

## IDE Setup (Pycharm)
Clone the project from GitHub and link it to PyCharm<br/>
Link the conda environment by going to<br/>
`Settings` -> `Project: data-evaluator` -> `Python Interpreter` ->  `Add Interpeter` (right top corner) -> `Add local interpreter` -> `Conda environment` -> `Use existing environment` -> Select `data-evaluator` -> `OK`

## Githook setup (Linux)

Go to the directory `githooks` and add copy the file `pre-commit` to the directory `./.git/hooks` and change its settings to executable:<br/>
`chmod u+x ./.git/hooks/pre-commit`
in order to work for the hook. Keep the call for your OS and delete the other ones.

## Load existing conda environment
Load the environment from the root directory via<br/>
`conda env update -n data-evaluator -f ./env/conda-env.yaml`