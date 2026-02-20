const rawQuizdown = `
---
shuffleAnswers: true
shuffleQuestions: true
---

# If performed on a nonexistent file, all of the following commands will return a non-zero exit code except:

1. [x] touch
1. [ ] cat
1. [ ] mv
1. [ ] cp
1. [ ] rm

# Assume you are a new user and the directory \`/home/user/docs\` does not exist. Which of the following mkdir commands will successfully create the nested directories \`/home/user/docs/work\`? Check all that apply:

- [x] mkdir -p /home/user/docs/work
  > The -p or --parents flag allows mkdir to create parent directories as needed. This command will create all necessary intermediate directories, including docs.
- [x] mkdir --parents /home/user/docs/work
  > The -p or --parents flag allows mkdir to create parent directories as needed. This command will create all necessary intermediate directories, including docs.
- [x] mkdir /home/user/docs && mkdir /home/user/docs/work
  > This command sequence first attempts to create the docs directory and then creates the work directory inside it. Since docs does not exist, it will be created successfully, followed by the successful creation of work.
- [ ] mkdir /home/user/docs/work
  > This command will fail because the intermediate directory (/home/user/docs) does not exist. 

# If you run the following command on a nonexistent directory, what will happen?
\`\`\`bash
cd nonexistent-directory-name
\`\`\`

1. [x] The command will error out and do nothing
1. [ ] The directory will be created
1. [ ] The directory will be created AND you will navigate into it

# Which of the following commands change the directory to the current user's home directory? Check all that apply:

- [x] cd /home/$USER
  > This command changes the current directory to the home directory of the user specified by the $USER environment variable.
- [x] cd ~
  > This command changes the current directory to the home directory of the current user. The ~ symbol is a shortcut for the user's home directory.
- [x] cd
  > Without any arguments, cd defaults to changing the directory to the current user's home directory.
- [ ] cd .
  > The . symbol represents the current directory. So, this command essentially means "stay in the current directory."

# Assume that \`echo-test.txt\` is a new file. What will the final output be?
\`\`\`bash
echo 'Hello' > echo-test.txt
echo 'World' > echo-test.txt
echo 'Hello' >> echo-test.txt
cat echo-test.txt
\`\`\`

1. [x] World<br>Hello
1. [ ] Hello<br>World
1. [ ] Hello
1. [ ] World
1. [ ] cat: echo-test.txt: No such file or directory
`;

export { rawQuizdown }