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

    echo "Running Auto-grader"
    echo "\nAuto-grader fpr P6:"
    python3 autograder.py p6 ? -ff main.ipynb -rf result.json

    echo "\nAuto-grader for P5:"
    python3 autograder.py p5 ? -ff land.py

    echo "\nAuto-grader for P4:"
    python3 autograder.py p4 ? -ff main.py

    echo "\nAuto-grader for P3:"
    python3 autograder.py p3 ? -ff p3.zip

    echo "\nAuto-grader for P2:"
    python3 autograder.py p2 ? -ff bus.py

    echo "\nAuto-grader for P1:"
    python3 autograder.py p1 ? --test-cmd "python3 test.py" --result-file result.json
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
