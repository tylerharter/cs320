#!/bin/sh

#Adapted from https://stackoverflow.com/questions/3258243

cd $(dirname "$0")

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

run_grader() {
    export PYTHONDONTWRITEBYTECODE=1
    export AWS_SHARED_CREDENTIALS_FILE="~/.aws/credentials"

    echo "Running Auto-grader\n"

    echo "\nAuto-grader for P2:"
    python3 autograder.py p2 ? --test-cmd "python3 tester.py" --result-file results.json

    echo "\nAuto-grader for P1:"
    python3 autograder.py p1 ?
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
