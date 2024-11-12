!#/bin/bash

## Export conda environment and remove `prefix` line, since it points to the local installation
conda env export -n data-evaluator -f ./env/conda-env.yaml --from-history
sed -i '/^prefix:/d' ./env/conda-env.yaml