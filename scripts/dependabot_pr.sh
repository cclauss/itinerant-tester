#!/bin/bash

# Ensure the first command-line argument is provided
if [ -z "$1" ]; then
  echo "Error: No GitHub repository URL provided."
  echo "Usage: $0 <repository-url>"
  exit 1
fi

# Set REPO_URL to the first command-line parameter
REPO_URL=$1

# Set other variables
REPO_NAME=$(basename -s .git ${REPO_URL})  # Extract the repo name
BRANCH_NAME="dependabot"
PR_TITLE="Keep GitHub Actions up to date with GitHub's Dependabot"
PR_BODY=$(cat <<EOF
* [Keeping your actions up to date with Dependabot](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot)
* [Configuration options for the dependabot.yml file - package-ecosystem](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file#package-ecosystem)
EOF
)
DEPENDABOT_YML=$(cat <<EOF
# Keep GitHub Actions up to date with GitHub's Dependabot...
# https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot
# https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file#package-ecosystem
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    groups:
      github-actions:
        patterns:
          - "*"  # Group all Actions updates into a single larger pull request
    schedule:
      interval: weekly
EOF
)

# Clone the repository
gh repo clone ${REPO_URL}
cd ${REPO_NAME}

# Add upstream remote (not strictly necessary if using gh clone)
git remote add upstream ${REPO_URL}

# Get the default branch name dynamically
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')

# Create and checkout new branch
git checkout -b ${BRANCH_NAME}

# Copy the dependabot.yml file
cat <<EOF > .github/dependabot.yml
${DEPENDABOT_YML}
EOF

# Stage, commit the changes
git add .github/dependabot.yml
git commit -m"${PR_TITLE}"

# Push the new branch to origin
git push origin ${BRANCH_NAME}

# Create a pull request, using the dynamically determined default branch
gh pr create --title "${PR_TITLE}" --body "${PR_BODY}" --base ${DEFAULT_BRANCH} --head ${BRANCH_NAME}
