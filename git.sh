#!/bin/bash
current_date=$(date "+%Y-%m-%d")

commit_message=${1:-"Add new content ${current_date}"}
current_branch=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $current_branch"

if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Not inside a Git repository. Please initialize Git first."
    exit 1
fi

git add . --sparse
git status
git commit -m "$commit_message"
git push origin "$current_branch"
#git sparse-checkout reapply

echo "Git synchronization to branch $current_branch completed."
