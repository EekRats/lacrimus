#!/bin/bash
#SBATCH --job-name=lacrimus
#SBATCH --array=0-1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --time=12:00:00
#SBATCH --output=lacrimus_%A_%a.log

umask 077
mkdir -p "$HOME/onions/lacrimus"

~/mkp224o/mkp224o -B -q -y -j "$(nproc)" -f "$HOME/onions/filters.txt" > "$HOME/onions/lacrimus/${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.yaml"
