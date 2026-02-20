# Basc Script to Pull New Update from the rep

git config --global user.name "devcloudninjas"
git config --global user.email "devcloudninjas@gmail.com"
# Set GITHUB_TOKEN environment variable
git config --global user.password "$GITHUB_TOKEN"
git config credential.helper store

git status
git pull
echo 'Pleas Wait , Loading files from github...'
read