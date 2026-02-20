git config --global user.name "devcloudninjas"
git config --global user.email "devcloudninjas@gmail.com"
git config --global user.password "ghp_ck3mCz18sCiv2m9Ax6uj3pH2f7wHMI1Bsoua"
git config credential.helper store

git status
git add .
echo 'Enter the commit message:'
# shellcheck disable=SC2162
read commitMessage

git commit -m "$commitMessage"

#echo 'Enter the name of the branch:'
#read branch

#git push origin $branch
git push origin main

read