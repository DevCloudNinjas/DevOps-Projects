package devops_resource

type Engineer struct {
	Name  string `json:"name"`
	Id    string `json:"id"`
	Email string `json:"email"`
}

type Dev struct {
	Name      string      `json:"name"`
	Id        string      `json:"id"`
	Engineers []*Engineer `json:"engineers"`
}

type Ops struct {
	Name      string      `json:"name"`
	Id        string      `json:"id"`
	Engineers []*Engineer `json:"engineers"`
}

type DevOps struct {
	Id  string `json:"id"`
	Devs []*Dev `json:"dev"`
	Ops []*Ops `json:"ops"`
}
