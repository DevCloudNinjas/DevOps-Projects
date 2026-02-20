# Hands-on Linux-09 : Shell Scripting/Functions

Purpose of the this hands-on training is to teach the students how to use functions in shell.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- explain and use functions in shell.

## Outline

- Part 1 - Creating Functions

- Part 2 - Passing Arguments to Functions

- Part 3 - Returning Values from Functions

- Part 4 - Nested Functions

- Part 5 - Variables Scope

## Part 1 - Creating Functions

- A Bash function is a piece of code that only runs when it is called. Functions enable you to reuse code. We can call the functions numerous times.

- Create a folder and name it `functions`.

```bash
mkdir functions && cd functions
```

- It is pretty easy to declare and call a function. Create a `script` file named `functions.sh`. 

```bash
#!/bin/bash

Welcome () {
    echo "Welcome to Linux Lessons"
}

Welcome
```

- Make the script executable and execute it.

```bash
chmod +x functions.sh
./functions.sh
```

## Part 2 - Passing Arguments to Functions

- We can pass any number of arguments to the bash function in a similar way to passing command line arguments to a script. We simply supply them right after the function’s name, separated by a space. These parameters would be represented by $1, $2 and so on, corresponding to the position of the parameter after the function’s name.

- Let's update the `functions.sh` script to see this.

```bash
#!/bin/bash

Welcome () {
    echo "Welcome to Linux Lessons $1 $2 $3"
}

Welcome Joe Matt Timothy
```

- And execute it.

```bash
./functions.sh
```

## Part 3 - Returning Values from Functions

- Functions in other programming languages return a value when called. But, Bash functions don’t return a value when called. But we can define a return status similar to exit status of a command.

- When any shell command terminates, it returns an exit code, which indicates `0` for success and non-zero decimal number in the `1 - 255` range for failure. The special variable `$?` returns the exit status of the last executed command. Let's see this.

```bash
pwd
echo $?  #0
pwt  # It is wrong command
echo $?  #127
```

- When a bash function completes, its return value is the status of the last statement executed in the function. We can speciy return status by using the `return` keyword. We can think the `return` keyword as exit status of function. 

- Add `return 3` line to `Welcome function`.

```bash
#!/bin/bash

Welcome () {
    echo "Welcome to Linux Lessons $1 $2 $3"
    return 3
    }

Welcome Joe Matt Timothy
echo $?
```

- And execute it.

```bash
./functions.sh
```

## Part 4 - Nested Functions

- One of the useful features of functions is that they can call themselves and other functions. 

- Create a `script` file named `nested-functions.sh`.

```bash
#!/bin/bash

function_one () {
   echo "This is from the first function"
   function_two
}

function_two () {
   echo "This is from the second function"
}

function_one
```

- Make the script executable and execute it.

```bash
chmod +x nested-functions.sh
./nested-functions.sh
```

## Part 5 - Variables Scope

- Global variables are variables that can be accessed from anywhere in the script regardless of the scope. In Bash, by default all variables are defined as global, even if declared inside the function.
Local variables can be declared within the function body with the local keyword and can be used only inside that function. 

- Create a `script` file named `variables-scope.sh`.

```bash
#!/bin/bash

var1='global 1'
var2='global 2'

var_scope () {
  local var1='function 1'
  var2='function 2'
  echo -e "Inside function:\nvar1: $var1\nvar2: $var2"
}

echo -e "Before calling function:\nvar1: $var1\nvar2: $var2"

var_scope

echo -e "After calling function:\nvar1: $var1\nvar2: $var2"
```

- Make the script executable and execute it.

```bash
chmod +x variables-scope.sh
./variables-scope.sh
```