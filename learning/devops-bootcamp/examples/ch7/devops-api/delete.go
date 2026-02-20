package main

import (
	"errors"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp/examples/ch7/devops-resources"
)

func removeEngineerElement(engineers []*devops_resource.Engineer, engineer_id string) ([]*devops_resource.Engineer, error) {
	for i := range engineers {
		if engineers[i].Id == engineer_id {
			if len(engineers) == 1 {
				var empty []*devops_resource.Engineer
				return empty, nil
			}
			engineers[i] = engineers[len(engineers)-1]
			return engineers[:len(engineers)-1], nil
		}
	}
	return nil, errors.New("engineer not found and not deleted")
}

func removeDevElement(devs []*devops_resource.Dev, dev_id string) ([]*devops_resource.Dev, error) {
	for i := range devs {
		if devs[i].Id == dev_id {
			devs[i] = devs[len(devs)-1]
			return devs[:len(devs)-1], nil
		}
	}
	return nil, errors.New("developer not found and not deleted")
}

func removeOpElement(ops []*devops_resource.Ops, op_id string) ([]*devops_resource.Ops, error) {
	for i := range ops {
		if ops[i].Id == op_id {
			ops[i] = ops[len(ops)-1]
			return ops[:len(ops)-1], nil
		}
	}
	return nil, errors.New("engineer not found and not deleted")
}

// functions to delete resources from other resources//
func deleteEngineerFrom_Op(op_id string, engineer_id string) (bool, error) {

	_, err := findEngineer_by_Id(engineer_id)
	if err != nil {
		return false, errors.New(" Engineer doesn't exist ")
	}
	op_val, err := findOp_by_Id(op_id)
	if err != nil {
		return false, errors.New(" Operations group doesn't exist ")
	}
	_, err = findEngineerInOp_by_Id(op_val, engineer_id)
	if err != nil {
		return false, errors.New(" Engineer doesn't exists inside specified Operations group ")
	}
	for i := range operations {
		if operations[i].Id == op_id {
			operations[i].Engineers, err = removeEngineerElement(operations[i].Engineers, engineer_id)
			if err != nil {
				return false, errors.New(" Error: " + err.Error())
			}
		}
	}
	for i := range developer_operations {
		for j := range developer_operations[i].Ops {
			if developer_operations[i].Ops[j].Id == op_id {
				developer_operations[i].Ops[j].Engineers, err = removeEngineerElement(developer_operations[i].Ops[j].Engineers, engineer_id)
				if err != nil {
					return false, errors.New(" Error: " + err.Error())
				}
			}
		}
	}

	return true, nil

}

func deleteEngineerFrom_Dev(dev_id string, engineer_id string) (bool, error) {

	_, err := findEngineer_by_Id(engineer_id)
	if err != nil {
		return false, errors.New(" Engineer doesn't exist ")
	}
	dev_val, err := findDev_by_Id(dev_id)
	if err != nil {
		return false, errors.New(" Developer group doesn't exist ")
	}
	_, err = findEngineerInDev_by_Id(dev_val, engineer_id)
	if err != nil {
		return false, errors.New(" Engineer doesn't exists inside specified Developer group ")
	}
	for i := range developers {
		if developers[i].Id == dev_id {
			developers[i].Engineers, err = removeEngineerElement(developers[i].Engineers, engineer_id)
			if err != nil {
				return false, errors.New(" Error: " + err.Error())
			}
		}
	}
	for i := range developer_operations {
		for j := range developer_operations[i].Devs {
			if developer_operations[i].Devs[j].Id == dev_id {
				developer_operations[i].Devs[j].Engineers, err = removeEngineerElement(developer_operations[i].Devs[j].Engineers, engineer_id)
				if err != nil {
					return false, errors.New(" Error: " + err.Error())
				}
			}
		}
	}

	return true, nil

}

func deleteDevFrom_DevOps(devops_id string, dev_id string) (bool, error) {

	_, err := findDev_by_Id(dev_id)
	if err != nil {
		return false, errors.New(" Developer group doesn't exist ")
	}
	devops_val, err := findDevOps_by_Id(devops_id)
	if err != nil {
		return false, errors.New(" Developer Oerations group doesn't exist ")
	}
	_, err = findDevInDevOps_by_Id(devops_val, dev_id)
	if err != nil {
		return false, errors.New(" Developer doesn't exists inside specified Developer Operations group ")
	}

	for i := range developer_operations {
		if developer_operations[i].Id == devops_id {
			developer_operations[i].Devs, err = removeDevElement(developer_operations[i].Devs, dev_id)
			if err != nil {
				return false, errors.New(" Error: " + err.Error())
			}
		}
	}

	return true, nil

}

func deleteOpFrom_DevOps(devops_id string, op_id string) (bool, error) {

	_, err := findOp_by_Id(op_id)
	if err != nil {
		return false, errors.New(" Operations group doesn't exist ")
	}
	devops_val, err := findDevOps_by_Id(devops_id)
	if err != nil {
		return false, errors.New(" Developer Oerations group doesn't exist ")
	}
	_, err = findOpInDevOps_by_Id(devops_val, op_id)
	if err != nil {
		return false, errors.New(" Operations group doesn't exists inside specified Developer Operations group ")
	}

	for i := range developer_operations {
		if developer_operations[i].Id == devops_id {
			developer_operations[i].Ops, err = removeOpElement(developer_operations[i].Ops, op_id)
			if err != nil {
				return false, errors.New(" Error: " + err.Error())
			}
		}
	}

	return true, nil

}

// **************************************************//
// functions to delete resources//
func deleteDevOps(devops_id string) (bool, error) {
	_, err := findDevOps_by_Id(devops_id)
	if err != nil {
		return false, errors.New(" Developer Oerations group doesn't exist ")
	}
	for i := range developer_operations {
		if developer_operations[i].Id == devops_id {
			if len(developer_operations) == 1 {
				developer_operations = []*devops_resource.DevOps{}
				return true, nil
			}
			developer_operations[i] = developer_operations[len(developer_operations)-1]
			developer_operations = developer_operations[:len(developer_operations)-1]
		}
	}
	return true, nil
}

func deleteDev(dev_id string) (bool, error) {
	_, err := findDev_by_Id(dev_id)
	if err != nil {
		return false, errors.New(" Developer group doesn't exist ")
	}
	for i := range developers {
		if i < len(developers) && developers[i].Id == dev_id {
			if len(developers) == 1 {
				developers = []*devops_resource.Dev{}
			} else {
				developers, err = removeDevElement(developers, dev_id)
				if err != nil {
					return false, err
				}
			}
		}
	}
	for i := range developer_operations {
		for j := range developer_operations[i].Devs {
			if developer_operations[i].Devs[j].Id == dev_id {
				if len(developer_operations[i].Devs) == 1 {
					developer_operations[i].Devs = []*devops_resource.Dev{}
					return true, nil
				}
				developer_operations[i].Devs, err = removeDevElement(developer_operations[i].Devs, dev_id)
				if err != nil {
					return false, errors.New(" Error: " + err.Error())
				}
			}
		}
	}
	return true, nil
}

func deleteOp(op_id string) (bool, error) {
	_, err := findOp_by_Id(op_id)
	if err != nil {
		return false, errors.New(" Operations group doesn't exist ")
	}
	for i := range operations {
		if i < len(operations) && operations[i].Id == op_id {
			if len(operations) == 1 {
				operations = []*devops_resource.Ops{}
			} else {
				operations, err = removeOpElement(operations, op_id)
				if err != nil {
					return false, errors.New(" Error: " + err.Error())
				}
			}
		}
	}
	for i := range developer_operations {
		for j := range developer_operations[i].Ops {
			if developer_operations[i].Ops[j].Id == op_id {
				if len(developer_operations[i].Ops) == 1 {
					developer_operations[i].Ops = []*devops_resource.Ops{}
					return true, nil
				}
				developer_operations[i].Ops, err = removeOpElement(developer_operations[i].Ops, op_id)
				if err != nil {
					return false, errors.New(" Error: " + err.Error())
				}
			}
		}
	}
	return true, nil
}

func deleteEngineer(engineer_id string) (bool, error) {
	_, err := findEngineer_by_Id(engineer_id)
	if err != nil {
		return false, errors.New(" Engineer doesn't exist ")
	}
	for i := range developers {
		for j := range developers[i].Engineers {
			if developers[i].Engineers[j].Id == engineer_id {
				developers[i].Engineers, err = removeEngineerElement(developers[i].Engineers, engineer_id)
				if err != nil {
					return false, errors.New(" Error: " + err.Error())
				}
			}
		}
	}
	for i := range operations {
		for j := range operations[i].Engineers {
			if operations[i].Engineers[j].Id == engineer_id {
				operations[i].Engineers, err = removeEngineerElement(operations[i].Engineers, engineer_id)
				if err != nil {
					return false, errors.New(" Error: " + err.Error())
				}
			}
		}
	}
	engineers, err = removeEngineerElement(engineers, engineer_id)
	if err != nil {
		return false, errors.New(" Error: " + err.Error())
	}

	return true, nil
}

// server DELETE handler
func deleteRequestEngineer(c *gin.Context) {
	id := c.Param("id")
	_, err := deleteEngineer(id)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"success": "engineer resource deleted"})
}

func deleteRequestDev(c *gin.Context) {
	id := c.Param("id")
	_, err := deleteDev(id)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"success": "developer resource deleted"})
}

func deleteRequestOp(c *gin.Context) {
	id := c.Param("id")
	_, err := deleteOp(id)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"success": "operations resource deleted"})
}

func deleteRequestDevOps(c *gin.Context) {
	id := c.Param("id")
	_, err := deleteDevOps(id)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"success": "developer operations resource deleted"})
}
