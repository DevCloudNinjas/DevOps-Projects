# Hands-on Linux-04 : Using Package Managers in Linux
​
Purpose of the this hands-on training is to teach the students how to use package managers in Linux.
​
## Learning Outcomes
​
At the end of the this hands-on training, students will be able to;
​
- Explain what is package management.
​
- Work with most common package management tools.
​
- Install, upgrade, configure and remove software packages using package management tools.
​
## Outline
​
- Part 1 - Using package managers ('yum' and 'apt') 
​
## Part 1 - Using Package Managers ('yum' and 'apt')
​
- Update Amazon Linux Instance.
​
```bash
sudo yum update
```
- Update Ubuntu's package list. This command updates the local repo database but do not install any package.
​
```bash
sudo apt update
```
- Upgrade the packages. This command installs the listed available packages.

```bash
sudo apt upgrade
```

- Check if 'git' is installed on Amazon Linux instance.
​
```bash
git --version
```
- Check if 'git' is installed on Ubuntu instance.
​
```bash
git --version
```
- Install git on Amazon Linux instance.
​
```bash
sudo yum install git
```
- Uninstall git on Amazon Linux instance.
​
```bash
sudo yum remove git
```
- Install git on Amazon Linux instance without any interruption.
​
```bash
sudo yum install git -y
```
- Uninstall git on Amazon Linux instance without any interruption.
​
```bash
sudo yum remove git -y
```
- Check the version of git installed on Amazon Linux instance.(There should be no info, because it's just removed a minute ago)
​
```bash
git --version
```
- Explain why there is still version info.
- Install git on Amazon Linux instance without any interruption.
​
```bash
sudo yum install git -y
```
- Uninstall git with dependencies on Amazon Linux instance without any interruption.
​
```bash
sudo yum autoremove git -y
```
- Check the version of git installed on Amazon Linux instance.(There should ne no info, because it's just removed a minute ago)
​
```bash
git --version
```
- Uninstall git on Ubuntu instance.
​
```bash
sudo apt remove git
```
- Check the version of git installed on Ubuntu instance.(There should be no info, because it's just removed a minute ago)
​
```bash
git --version
```
- Install git on Ubuntu instance without any interruption.
​
```bash
sudo apt install git -y
```
- Uninstall git with dependencies on Ubuntu instance without any interruption.
​
```bash
sudo apt autoremove git -y
```
- Check the info for the git package installed on Amazon Linux instance.
​
```bash
sudo yum info git
```
- Check the info for the git package installed on Ubuntu instance.
​
```bash
sudo apt info git
```
- List all available packages for Amazon Linux instance.
​
```bash
sudo yum list
```
- List all available packages for Ubuntu instance.
​
```bash
sudo apt list
```
- List all available git packages for Amazon Linux instance.
​
```bash
sudo yum list git
```
- List all available git packages for Ubuntu instance.
​
```bash
sudo apt list git
```
- List all installed packages on Amazon Linux instance.
​
```bash
sudo yum list installed
```
- List all installed packages on Ubuntu instance.
​
```bash
sudo apt list --installed
```
- List all available versions of git packages on Amazon Linux instance.
​
```bash
sudo yum --showduplicates list git
```
- Check the version of git installed on Amazon Linux instance.
​
```bash
git --version
```
- Uninstall git with dependencies on Amazon Linux instance without any interruption.
​
```bash
sudo yum autoremove git -y
```
- Install a previous version of git on Amazon Linux instance.
​
```bash
sudo yum --showduplicates list git
sudo yum install git-2.14.5-1.amzn2 -y
```
- Check the version of git installed on Amazon Linux instance.
​
```bash
git --version
```
- List all available versions of git packages on Amazon Linux instance.
​
```bash
sudo yum --showduplicates list git
``` 
- Check the available version of git with info command.
​
```bash
sudo yum list git
```
- Update git and check the version.
​
```bash
sudo yum update git -y
git --version
```
