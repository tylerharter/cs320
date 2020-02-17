#!/bin/sh

#Adapted from https://stackoverflow.com/questions/3258243

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

run_grader() {
    echo "Running Auto-grader\n"

    echo "\nAuto-grader for P1:"
    python3 autograder.py p1 ? -ff main.ipynb -c
}

ntpdate -s time.nist.gov
git fetch

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
    run_grader
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    git pull
    run_grader
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
else
    echo "Diverged"
fi
