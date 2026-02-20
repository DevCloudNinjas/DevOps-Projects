# DevOps resource struct module

#### This module is used and consumed by the devops rest api and custom terraform provider for bootcamp section 7.1.4. Its purpose is to organize the structure of the resources defined in this bootcamp section in order to lessen the strain in having to set up structures for client-side communication for the terraform custom provider to talk to the devops api.

## How to import module for the resources built in go:

### Example in how the import is call in your go code:

```go
import "learning/devops-bootcamp/examples/ch7/devops-resources"
```

#### This is how you would pull the module in the default branch [master]

### If you are trying to pull the module from a branch that differs from the default branch then you can do this step:

#### Here is an example of how to include the module inside of the go.mod within the terraform provider:

```go
require learning/devops-bootcamp/examples/ch7/devops-resource [branch]
```

#### When you run go mod tidy go will look for the module at the head of the branch you specified in go.mod

### Now that you have the right path targeted for the import you can now use this module for any code corresponding to client-side communication from the terraform provider to the devops api.

## How to call package devops_resource:

#### To access struct type that is defined in the module you call it like this:

##### Engineer Struct:

```go
devops_resource.Engineer
```

##### Dev Struct:

```go
devops_resource.Dev
```

##### Ops Struct:

```go
devops_resource.Ops
```

##### DevOps Struct:

```go
devops_resource.DevOps
```

## Notes:

### The structs use references of another struct object to manage lists.

- This allows easier management of the lists when updating a resource.

#### Struct Example:

```go
type DevOps struct {
        Id  string `json:"id"`
        Devs []*Dev `json:"dev"`
        Ops []*Ops `json:"ops"`
}
```

##### DevOps Struct is a good example of this since it manages a list of type Dev and Ops.

### Why is the module name long and almost looks like a path.

- Go looks for the path in which the package and module is referenced.
- For this case the repository is github.com(host)/devcloudninjas(owner)/devops-bootcamp(repo)/examples/ch7/devops-resources(path to package)
