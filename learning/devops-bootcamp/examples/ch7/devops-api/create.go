package main

import (
	"errors"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp/examples/ch7/devops-resources"
)

func newDevOps(newDevOps devops_resource.DevOps) (*devops_resource.DevOps, error) {
	devOpsGroup := devops_resource.DevOps{Id: getRandId(5)}
	devOpsGroup.Ops = make([]*devops_resource.Ops, 0)
	devOpsGroup.Devs = make([]*devops_resource.Dev, 0)
	for _, newDev := range newDevOps.Devs {
		dev, err := findDev_by_Id(newDev.Id)
		if err != nil {
			return nil, errors.New(" Dev group doesnt exists ")
		}
		devOpsGroup.Devs = append(devOpsGroup.Devs, dev)
	}
	for _, newOp := range newDevOps.Ops {
		op, err := findOp_by_Id(newOp.Id)
		if err != nil {
			return nil, errors.New(" Ops group doesnt exists ")
		}
		devOpsGroup.Ops = append(devOpsGroup.Ops, op)
	}
	developer_operations = append(developer_operations, &devOpsGroup)
	return &devOpsGroup, nil
}

func newDev(newDev devops_resource.Dev) (*devops_resource.Dev, error) {
	if newDev.Name == "" {
		return nil, errors.New(" Name cannot be empty ")
	}
	for _, value := range developers {
		if newDev.Name == value.Name {
			return nil, errors.New(" Dev group already exists ")
		}
	}
	devGroup := devops_resource.Dev{Name: newDev.Name, Id: getRandId(5)}
	devGroup.Engineers = make([]*devops_resource.Engineer, 0)
	for _, eng := range newDev.Engineers {
		newEngineer, err := findEngineer_by_Id(eng.Id)
		if err != nil {
			return nil, errors.New(" engineer doesnt exists ")
		}
		devGroup.Engineers = append(devGroup.Engineers, newEngineer)
	}

	developers = append(developers, &devGroup)
	return &devGroup, nil
}

func newOp(newOp devops_resource.Ops) (*devops_resource.Ops, error) {
	if newOp.Name == "" {
		return nil, errors.New(" Name cannot be empty ")
	}
	for _, value := range operations {
		if newOp.Name == value.Name {
			return nil, errors.New(" Dev group already exists ")
		}
	}
	opsGroup := devops_resource.Ops{Name: newOp.Name, Id: getRandId(5)}
	opsGroup.Engineers = make([]*devops_resource.Engineer, 0)
	for _, eng := range newOp.Engineers {
		newEngineer, err := findEngineer_by_Id(eng.Id)
		if err != nil {
			return nil, errors.New(" engineer doesnt exists ")
		}
		opsGroup.Engineers = append(opsGroup.Engineers, newEngineer)
	}

	operations = append(operations, &opsGroup)
	return &opsGroup, nil
}

func newEngineer(name string, email string) (*devops_resource.Engineer, error) {
	if name == "" {
		return nil, errors.New(" Name cannot be empty ")
	}
	for _, value := range engineers {
		if name == value.Name {
			return nil, errors.New(" Engineer already exists ")
		}
	}
	if !verifyEmail(email) {
		return nil, errors.New(" Email is invalid ")
	}
	p := devops_resource.Engineer{Name: name, Id: getRandId(5)}
	p.Email = email
	engineers = append(engineers, &p)
	return &p, nil
}

func findEngineer_by_Id(engineer_id string) (*devops_resource.Engineer, error) {
	for _, newEngineer := range engineers {
		if newEngineer.Id == engineer_id {
			return newEngineer, nil
		}
	}
	return nil, errors.New(" No engineer with that ID ")
}

func findOp_by_Id(op_id string) (*devops_resource.Ops, error) {
	for _, newOp := range operations {
		if newOp.Id == op_id {
			return newOp, nil
		}
	}
	return nil, errors.New(" No ops group with that ID ")
}

func findDev_by_Id(dev_id string) (*devops_resource.Dev, error) {
	for _, newDev := range developers {
		if newDev.Id == dev_id {
			return newDev, nil
		}
	}
	return nil, errors.New(" No dev group with that ID ")
}

func findDevOps_by_Id(devops_id string) (*devops_resource.DevOps, error) {
	for _, newDevOps := range developer_operations {
		if newDevOps.Id == devops_id {
			return newDevOps, nil
		}
	}
	return nil, errors.New(" No devops group with that ID ")
}

func findEngineerInOp_by_Id(op *devops_resource.Ops, engineer_id string) (*devops_resource.Engineer, error) {
	for _, newEngineer := range op.Engineers {
		if newEngineer.Id == engineer_id {
			return newEngineer, nil
		}
	}
	return nil, errors.New(" No engineer with that ID in this ops group")
}

func findEngineerInDev_by_Id(dev *devops_resource.Dev, engineer_id string) (*devops_resource.Engineer, error) {
	for _, newEngineer := range dev.Engineers {
		if newEngineer.Id == engineer_id {
			return newEngineer, nil
		}
	}
	return nil, errors.New(" No engineer with that ID in this dev group ")
}

func findDevInDevOps_by_Id(devops *devops_resource.DevOps, dev_id string) (*devops_resource.Dev, error) {
	for _, newDev := range devops.Devs {
		if newDev.Id == dev_id {
			return newDev, nil
		}
	}
	return nil, errors.New(" No dev with that ID in this devops group")
}

func findOpInDevOps_by_Id(devops *devops_resource.DevOps, op_id string) (*devops_resource.Ops, error) {
	for _, newOp := range devops.Ops {
		if newOp.Id == op_id {
			return newOp, nil
		}
	}
	return nil, errors.New(" No op with that ID in this devops group")
}

// functions to add resources to other resources//
func addEngineerTo_Op(ops_id string, engineer_id string) (bool, error) {

	engineer_val, err := findEngineer_by_Id(engineer_id)
	if err != nil {
		return false, errors.New(" Engineer doesn't exist ")
	}
	op_val, err := findOp_by_Id(ops_id)
	if err != nil {
		return false, errors.New(" Operations group doesn't exist ")
	}
	_, err = findEngineerInOp_by_Id(op_val, engineer_id)
	if err == nil {
		return false, errors.New(" Engineer already exists inside specified Operations group ")
	}
	for i := range operations {
		if operations[i].Id == ops_id {
			operations[i].Engineers = append(operations[i].Engineers, engineer_val)
		}
	}

	return true, nil

}

func addEngineerTo_Dev(dev_id string, engineer_id string) (bool, error) {

	engineer_val, err := findEngineer_by_Id(engineer_id)
	if err != nil {
		return false, errors.New(" Engineer doesn't exist ")
	}
	dev_val, err := findDev_by_Id(dev_id)
	if err != nil {
		return false, errors.New(" Developer group doesn't exist ")
	}
	_, err = findEngineerInDev_by_Id(dev_val, engineer_id)
	if err == nil {
		return false, errors.New(" Engineer already exists inside specified Developer group ")
	}

	for i := range developers {
		if developers[i].Id == dev_id {
			developers[i].Engineers = append(developers[i].Engineers, engineer_val)
		}
	}

	return true, nil

}

func addDevTo_DevOps(devops_id string, dev_id string) (bool, error) {

	dev_val, err := findDev_by_Id(dev_id)
	if err != nil {
		return false, errors.New(" Developer group doesn't exist ")
	}
	devops_val, err := findDevOps_by_Id(devops_id)
	if err != nil {
		return false, errors.New(" Developer Operations group doesn't exist ")
	}
	_, err = findDevInDevOps_by_Id(devops_val, dev_id)
	if err == nil {
		return false, errors.New(" Developer already exists inside specified Developer Operations group ")
	}
	for i := range developer_operations {
		if developer_operations[i].Id == devops_id {
			developer_operations[i].Devs = append(developer_operations[i].Devs, dev_val)
		}
	}

	return true, nil

}

func addOpTo_DevOps(devops_id string, op_id string) (bool, error) {

	op_val, err := findOp_by_Id(op_id)
	if err != nil {
		return false, errors.New(" Developer group doesn't exist ")
	}
	devops_val, err := findDevOps_by_Id(devops_id)
	if err != nil {
		return false, errors.New(" Developer Operations group doesn't exist ")
	}
	_, err = findOpInDevOps_by_Id(devops_val, op_id)
	if err == nil {
		return false, errors.New(" Developer already exists inside specified Developer Operations group ")
	}
	for i := range developer_operations {
		if developer_operations[i].Id == devops_id {
			developer_operations[i].Ops = append(developer_operations[i].Ops, op_val)
		}
	}

	return true, nil

}

// server POST handlers
func postEngineer(c *gin.Context) {
	var jsonData devops_resource.Engineer     //object that gets name and email from POST request
	var curEngineer *devops_resource.Engineer //object recieved from newEngineer

	err := c.BindJSON(&jsonData)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	curEngineer, err = newEngineer(jsonData.Name, jsonData.Email)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	engineer, err := findEngineer_by_Id(curEngineer.Id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusCreated, engineer)
}

func postDev(c *gin.Context) {
	var jsonData devops_resource.Dev //object that gets dev data from POST request
	var curDev *devops_resource.Dev  //object recieved from newDev

	err := c.BindJSON(&jsonData)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	curDev, err = newDev(jsonData)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusCreated, curDev)
}

func postOp(c *gin.Context) {
	var jsonData devops_resource.Ops //object that gets dev data from POST request
	var curOp *devops_resource.Ops   //object recieved from newOp

	err := c.BindJSON(&jsonData)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	curOp, err = newOp(jsonData)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	op, err := findOp_by_Id(curOp.Id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusCreated, op)

}

func postDevOps(c *gin.Context) {
	var jsonData devops_resource.DevOps
	err := c.BindJSON(&jsonData)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	curDevOps, err := newDevOps(jsonData)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	devops, err := findDevOps_by_Id(curDevOps.Id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.IndentedJSON(http.StatusCreated, devops)
}

func postDevEngineer(c *gin.Context) {
	id := c.Param("id") //dev id
	var jsonData devops_resource.Engineer
	err := c.ShouldBindJSON(&jsonData)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	_, err = addEngineerTo_Dev(id, jsonData.Id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	dev, err := findDev_by_Id(id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, dev)
}

func postOpEngineer(c *gin.Context) {
	id := c.Param("id") //op id
	var jsonData devops_resource.Engineer
	err := c.ShouldBindJSON(&jsonData)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	_, err = addEngineerTo_Op(id, jsonData.Id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	op, err := findOp_by_Id(id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, op)
}

func postDevOpsDev(c *gin.Context) {
	id := c.Param("id") //devops id
	var jsonData devops_resource.Dev

	err := c.ShouldBindJSON(&jsonData)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	_, err = addDevTo_DevOps(id, jsonData.Id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	devops, err := findDevOps_by_Id(id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, devops)
}

func postDevOpsOp(c *gin.Context) {
	id := c.Param("id") //devops id
	var jsonData devops_resource.Ops

	err := c.ShouldBindJSON(&jsonData)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	_, err = addOpTo_DevOps(id, jsonData.Id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	devops, err := findDevOps_by_Id(id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, devops)
}
