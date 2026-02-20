const rawQuizdown = `
# Is this a quiz?

1. [x] True
1. [ ] False

# Please bring the following into sequence!

That's **super easy**!

1. One
2. Two
3. Three
4. Four
5. Five

# Python Lists

Testing syntax highlighting

\`\`\`python
# Python
x = [2, 3, 4]
y = "string"
x[2] = 4
print(x[2])
\`\`\`

\`\`\`bash
# Bash
y = "string"
echo $y
rm -rf /
aws-vault exec nick-is-awesome -- aws s3 ls
\`\`\`

\`\`\`js
// Javascript
const x = [2, 3, 4]
x[2] = 4
let y = 'string'
console.log(x[2])
\`\`\`

\`\`\`json
{
  "name":"John",
  "age":30,
  "car":null
}
\`\`\`

\`\`\`go
// GO
package main
import "fmt"
func main() {
    fmt.Println("hello world")
}
\`\`\`

\`\`\`yaml
# yml
on:
  push:
    branches: ["master"]

permissions:
  contents: read
  pages: write
  id-token: write
\`\`\`

- [x] NEXT!

# Who's that DevCloud Ninja?

![](https://i.ibb.co/CJM63dp/somebody.png)

> Doesn't matter, they all look the same!
> ![](https://i.ibb.co/D1tQkJz/image-4.png)

- [x] Joe Wood
  > Sure, why not!
- [x] Robert Kelly
  > Sure, why not!
- [x] Andrei Titerlea
  > Sure, why not!
- [x] Eric Chapman
  > Sure, why not!
- [x] Nicholas Shaddox
  > Sure, why not!
`;

export { rawQuizdown }