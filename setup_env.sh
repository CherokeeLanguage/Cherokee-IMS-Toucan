#!/usr/bin/env bash

set -e
set -o pipefail
cd "$(dirname "$0")" || exit 1
eval "$(conda shell.bash hook)"

env="$(grep name: environment.yml|cut -f 2 -d ':'|xargs)"

conda deactivate
conda create -n "$env" python=3.8 --no-default-packages --force
conda activate "$env"
conda config --env --set channel_priority flexible
conda env update -f environment.yml

cd IMS_Toucan
pip install -e .

exit 0
