# Hands-on Linux-02 : Linux Environment Variables

Purpose of the this hands-on training is to teach the students how to use environment variables.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- explain environment variables.

- understand Quoting with Variables.

## Outline

- Part 1 - Common Environment Variables & Accessing Variable

- Part 2 - Path Variable

- Part 3 - Quoting with Variables

- Part 4 - Sudo Command

## Part 1 - Common Environment/Shell Variables & Accessing Variable
​
- Difference between "env" and "printenv" commands.
​
```bash
env
printenv
printenv HOME
echo $HOME
env HOME
```
​
- Understanding the shell variable.
​
```bash
CLARUS=way
env
set
set | grep CLARUS
echo $CLARUS
```
​
- Understanding the environment variable. Use export command.
​
```bash
export WAY=clarus
env
```
​
- Difference between shell and environment variables. Create a user, name it "user1", switch to user1, check the environment and shell variables.
​
```bash
export WAY=clarus
sudo su
useradd user1
passwd user1 # give user1 any password.
exit
su user1
env | grep WAY
set | grep CLARUS
```
​
- Change the environment variable value.
​
```bash
export WAY=linux
env
export WAY=script
env
```
​
- Remove the environment variable with unset command.
​
```bash
export WAY=road
env | grep WAY
unset WAY
env | grep WAY
```
​
## Part 2 - Path Variable
​
- PATH variable.
​
```bash
printenv PATH
cd /bin
ls ca*    # see the cat command.
```
​
- Add a path to PATH variable for running a script.
​
```bash
cd
mkdir test && cd test
nano test.sh
# copy and paste the code-echo "hello world"- in test.sh
chmod +x test.sh
./test.sh
cd    # change directory to ec2-user's home directory
./test.sh    # it doesnt work. 
./test/test.sh
printenv PATH
cd test
pwd
export PATH=$PATH:/home/ec2-user/test
printenv PATH
cd
test.sh
cd /
test.sh
```
​
- Using the environment variable in the script.
​
```bash
cd test
export CLARUS=env.var
WAY=shell.var
cd test
nano test1.sh
# copy and paste the code- echo "normally we should see env. variable $CLARUS but probably we can't see the shell variable $WAY "
chmod +x test1.sh
./test1.sh
```
​
## Part 3 - Quoting with Variables.
​
- Double Quotes.
​
```bash
MYVAR=my value
echo $MYVAR
MYVAR="my value"
echo $MYVAR
MYNAME=james
MYVAR="my name is $MYNAME"
echo $MYVAR
MYNAME="james"
MYVAR="hello $MYNAME"
echo $MYVAR
MYVAR="hello \$MYNAME"
echo $MYVAR
```
​
- Single Quotes.
​
```bash
echo '$SHELL'
echo 'My\$SHELL'
```
​
## Part 4 - Sudo Command.
​
- Sudo Command.
​
```bash
yum update
sudo yum update
cd /
mkdir testfile
sudo su
sudo -s
sudo su -
```