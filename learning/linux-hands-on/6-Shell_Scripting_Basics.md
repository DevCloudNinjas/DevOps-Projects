# Hands-on Linux-06 : Shell Scripting Basics

Purpose of the this hands-on training is to teach the students how to script in shell.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- explain shell scripting basics.

- explain shell variables.

- do simple arithmetic.

## Outline

- Part 1 - Shell Scripting Basics

- Part 2 - Shell Variables

- Part 3 - Simple Arithmetic

## Part 1 - Shell Scripting Basics

- Create a folder and name it shell-scripting.

```bash
mkdir shell-scripting && cd shell-scripting
```

- Create a `script` file named `basic.sh`. Note all the scripts would have the .sh extension.

```bash
#!/bin/bash
echo "Hello World"
```

- Before we add anything else to our script, we need to alert the system that a shell script is being started.
This is done specifying `#!/bin/bash` on the first line, meaning that the script should always be run with bash, rather than another shell. `#!` is called a `shebang` because the `#` symbol is called a hash, and the `!` symbol is called a bang.

- After to save the above content, we need to make the script executable.

```bash
chmod +x basic.sh
```

- Then we can execute the `basic.sh`. To execute basic.sh, it is required to add `./` beginning of the `basic.sh`. `./` means we're calling something in the current working directory. We have to specify the path for executables if they're outside our $PATH variable.

```bash
./basic.sh
```

- We can add the other shell commands to our script.

```bash
#!/bin/bash
echo "hello"
date
pwd
ls
```

- And execute again.

```bash
./basic.sh
```

### Shell Comments

- Bash ignores everything written on the line after the hash mark `(#)`. The only exception to this rule is the first line of the script that starts with the `#!` characters. 

- Comments can be added at the beginning on the line or inline with other code. Let's update `basic.sh`.

```bash
#!/bin/bash
echo "hello"
# date
pwd # This is an inline comment
# ls
```

- Unlike most of the programming languages, Bash doesn’t support multiline comments. But, we can use `here document` for this. In Linux, here document (also commonly referred to as `heredoc`) refers to a special block of code that contains multi-line strings that will be redirected to a command. If the `HereDoc block` is not redirected to a command, it can serve as a multiline comments placeholder.

### HEREDOC syntax

- A heredoc consists of the **<<** `(redirection operator)`, followed by a delimiter token. After the delimiter token, lines of string can be defined to form the content. Finally, the delimiter token is placed at the end to serve as the termination. The delimiter token can be any value as long as it is unique enough that it won’t appear within the content.

- Let's see how to use HereDoc.

```bash
cat << EOF
Welcome to the Linux Lessons.
This lesson is about the shell scripting
EOF
```

- Update the `basic.sh`.

```bash
#!/bin/bash
echo "hello"
# date
pwd # This is an inline comment
# ls

cat << EOF
Welcome to the Linux Lessons.
This lesson is about the shell scripting
EOF

<< multiline-comment
pwd
ls
Everything inside the
HereDoc body is
a multiline comment
multiline-comment
```

- Execute the basic.sh.

```bash
./basic.sh
```

## Part 2 - Shell Variables

- A variable is pointer to the actual data. The shell enables us to create, assign, and delete variables.

- The name of a variable can contain only letters (a to z or A to Z), numbers ( 0 to 9) or the underscore character (_) and beginning with a letter or underscore character.

- The following examples are valid variable names.

```bash
KEY=value
_VAR=5
clarus_way=test
```

> Note that there is no space on either side of the equals ( = ) sign. 

- The following examples are invalid.

```bash
3_KEY=value
-VAR=5
clarus-way=test
KEY_1?=value1
```

- The reason we cannot use other characters such as `?`, `*`, or `-` is that these characters have a special meaning for the shell.

- Create a new file and name it `variable.sh`.

```bash
#!/bin/bash
NAME=Joe
echo $NAME
```

- Make the script executable and then execute it.

```bash
chmod +x variable.sh && ./variable.sh
```

### Command Substitution

- Command substitution empowers us to take the output of a command or program (which would usually be written on the screen) and save it as the value of a variable. To do this we put it inside brackets, followed by a $ symbol.

```bash
content=$(ls)
echo $content
```

- or we can use `(backtick)

```bash
content=`ls`
echo $content
```

- let's see that in a script. Create a file and name it `command-substitution.sh`.

```bash
#!/bin/bash
working_directory=$(pwd)
echo "Welcome, your working directory is $working_directory."
```

- Make the script executable and execute it. 

```bash
chmod +x command-substitution.sh
./command-substitution.sh
```

- We can also get same result without using variables. Update the `command-substitution.sh` file as below.

```bash
#!/bin/bash
echo "Welcome, your working directory is $(pwd)."
echo "Today is `date`"
echo "You are `whoami`"
```

- And execute it. 

```bash
./command-substitution.sh
```

### Console input

- The Bash `read` command is a powerful built-in utility used take user input. 

- Update the `variable.sh` file.

```bash
#!/bin/bash
echo "Enter your name: "
read NAME
echo "Welcome $NAME"
```

- When writing interactive bash scripts, we can use the read command to get the user input. To specify a prompt string, use the -p option. The prompt is printed before the read is executed and doesn’t include a newline.

```bash
read -p "Enter your name: " NAME
echo "Welcome $NAME"
```

- When entering sensitive information we do not want to display input coming. For this we can use `read -s`

```bash
read -p "Enter your name: " NAME
echo "Welcome $NAME"

read -s -p "Enter your password: " PASSWORD
echo -e "\nYour password is $PASSWORD"
```

### Command Line Arguments

- Command-line arguments are given after the name of the program in command-line shell of Operating Systems. The command-line arguments $1, $2, $3, ...$9 are positional parameters, with $0 pointing to the actual command, program, shell script, or function and $1, $2, $3, ...$9 as the arguments to the command.

- Create a new file and name it `argument.sh`.

```bash
#!/bin/bash
echo "File Name is $0"
echo "First Parameter is $1"
echo "Second Parameter is $2"
echo "Third Parameter is $3"
echo "All the Parameters are $@"
echo "Total Number of Parameters : $#"
echo "$RANDOM is a random number"
echo "The current line number is $LINENO"
```

- Make the script executable. 

```bash
chmod +x argument.sh
```

- Execute it with following command.

```bash
./argument.sh Joe Matt Timothy James Guile
```

### Arrays

- In our programs, we usually need to group several values to render as a single value. In shell, arrays can hold multiple values at the same time.

#### Defining arrays

- Following is the simplest method of creating an array variable. 

```bash
DISTROS[0]="ubuntu"
DISTROS[1]="fedora"
DISTROS[2]="debian"
DISTROS[3]="centos"
DISTROS[4]="alpine"
```

- We can also use following method.

```bash
devops_tools=("docker" "kubernetes" "ansible" "terraform" "jenkins")
```

#### Working with arrays

- We can access a value in an array by using the following method.

```bash
echo ${DISTROS[0]}
echo ${DISTROS[1]}
```

- We can access all elements by putting `@` instead of number.

```bash
echo ${DISTROS[@]}
```

- With the following method, we can learn number of elements.

```bash
echo ${#DISTROS[@]}
```

## Part 3 - Simple Arithmetic

- There are many ways to evaluate arithmetic expression in Bash scripting

### expr

- `expr` command print  the value of expression to standard output. Let's see this.

```bash
expr 3 + 5
expr 6 - 2
expr 7 \* 3
expr 9 / 3
expr 7 % 2
```

- Using `expr` command, we must have spaces between the items of the expression and must not put quotes around the expression. If we do that, the expression will not be evaluated but printed instead. See the difference.

```bash
expr "3 + 5"
expr 3-2
```

- Let's create a simple calculator. Create a file and name it `calculator.sh`.

- Make the script executable. 

```bash
chmod +x calculator.sh
```

```bash
#!/bin/bash
read -p "Input first number: " first_number
read -p "Input second number: " second_number

echo "SUM="`expr $first_number + $second_number`
echo "SUB="`expr $first_number - $second_number`
echo "MUL="`expr $first_number \* $second_number`
echo "DIV="`expr $first_number / $second_number`
```

> How can we do with Command Line Arguments?

### let

- `let` is a builtin function of Bash that helps us to do simple arithmetic. It is similar to `expr` except instead of printing the answer it saves the result to a variable. Unlike expr we need to enclose the expression in quotes. 

```bash
let "sum = 3 + 5"
echo $sum
```

- Note that if we don't put quotes around the expression then it must be written with no spaces.

```bash
let sub=8-4
echo $sub
```

- We can also increase or decrease the variable by 1 with `let` function. Let's see this.

```bash
x=5
let x++
echo $x

y=3
let y--
echo $y
```

- Create a file and name it `let-calculator.sh`.

```bash
#!/bin/bash
read -p "Input first number: " first_number
read -p "Input second number: " second_number

let "sum = $first_number + $second_number"
let "sub = $first_number - $second_number"
let "mul = $first_number * $second_number"
let "div = $first_number / $second_number"
echo "SUM=$sum"
echo "SUB=$sub"
echo "MUL=$mul"
echo "DIV=$div"

let first_number++
let second_number--
echo "The increment of first number is $first_number"
echo "The decrement of second number is $second_number"
```

- Make the script executable and execute it. 

```bash
chmod +x let-calculator.sh
./let-calculator.sh
```

#### Difference between `num++` and `++num`, or `num--` and `--num`

- Create a file and name it number.sh.

```bash
number=10
let new_number=number++   # This firstly assigns the number then increases.
echo "Number = $number"
echo "New number = $new_number"

number=10
let new_number=--number   # This firstly decreases the number then assigns.
echo "Number = $number"
echo "New number = $new_number"
```

- Make the script executable and execute it. 

```bash
chmod +x number.sh
./number.sh
```

### Double Parentheses

- We can also evaluate arithmetic expression with double parentheses. We have learned that we could take the output of a command and save it as the value of a variable. We can use this method to do basic arithmetic.

```bash
sum=$((3 + 5))
echo $sum
```

- As we can see below, it works just the same if we take spacing out.

```bash
sum=$((3+5))
echo $sum
```

- Create a file and name it `parantheses-calculator.sh`.

```bash
#!/bin/bash
read -p "Input first number: " first_number
read -p "Input second number: " second_number

sum=$(($first_number + $second_number)) 
sub=$(($first_number - $second_number)) 
mul=$(($first_number * $second_number)) 
div=$(($first_number / $second_number)) 


echo "SUM=$sum"
echo "SUB=$sub"
echo "MUL=$mul"
echo "DIV=$div"

(( first_number++ ))
(( second_number-- ))

echo "The increment of first number is $first_number"
echo "The decrement of second number is $second_number"
```

- Make the script executable and execute it. 

```bash
chmod +x parantheses-calculator.sh
./parantheses-calculator.sh
```