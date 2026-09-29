#!/bin/bash
#SBATCH --job-name=lacrimus
#SBATCH --partition=pre
#SBATCH --exclude=gpu[01-04],lm[01-03]
#SBATCH --array=0-7
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --nice=10000
#SBATCH --requeue
#SBATCH --time=12:00:00
#SBATCH --output=lacrimus_%A_%a.log

umask 077
mkdir -p "$HOME/onions/lacrimus"

~/mkp224o/mkp224o -B -q -y -j "$(nproc)" -f "$HOME/onions/filters.txt" >> "$HOME/onions/lacrimus/${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.yaml"
