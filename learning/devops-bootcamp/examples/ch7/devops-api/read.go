package main

import (
	"errors"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp/examples/ch7/devops-resources"
)

func findEngineer_by_Name(engineer_name string) (*devops_resource.Engineer, error) {
	for _, newEngineer := range engineers {
		if newEngineer.Name == engineer_name {
			return newEngineer, nil
		}
	}
	return nil, errors.New(" no engineer with that name ")
}

func findEngineer_by_Email(engineer_email string) (*devops_resource.Engineer, error) {
	for _, newEngineer := range engineers {
		if newEngineer.Email == engineer_email {
			return newEngineer, nil
		}
	}
	return nil, errors.New(" no engineer with that email ")
}

func findDev_by_Name(dev_name string) (*devops_resource.Dev, error) {
	for _, newDev := range developers {
		if newDev.Name == dev_name {
			return newDev, nil
		}
	}
	return nil, errors.New(" no dev group with that name ")
}

func findOps_by_Name(ops_name string) (*devops_resource.Ops, error) {
	for _, newOps := range operations {
		if newOps.Name == ops_name {
			return newOps, nil
		}
	}
	return nil, errors.New(" no ops group with that name ")
}

func getSpecificEngineerById(c *gin.Context) {
	id := c.Param("id")

	engineer, err := findEngineer_by_Id(id)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, engineer)
}

func getSpecificEngineerByName(c *gin.Context) {
	name := c.Param("name")

	engineer, err := findEngineer_by_Name(name)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, engineer)
}

func getSpecificEngineerByEmail(c *gin.Context) {
	email := c.Param("email")

	engineer, err := findEngineer_by_Email(email)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, engineer)
}

func getSpecificDevById(c *gin.Context) {
	id := c.Param("id")

	dev, err := findDev_by_Id(id)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	//dev_slice := devToDevEngineer(dev)
	c.IndentedJSON(http.StatusOK, dev)
}

func getSpecificDevByName(c *gin.Context) {
	name := c.Param("name")

	dev, err := findDev_by_Name(name)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, dev)
}

func getSpecificOpsById(c *gin.Context) {
	id := c.Param("id")

	ops, err := findOp_by_Id(id)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	//ops_slice := opsToOpsEngineer(ops)
	c.IndentedJSON(http.StatusOK, ops)

}

func getSpecificOpsByName(c *gin.Context) {
	name := c.Param("name")

	ops, err := findOps_by_Name(name)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, ops)
}

func getSpecificDevOpsById(c *gin.Context) {
	id := c.Param("id")

	devops, err := findDevOps_by_Id(id)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	//ops_slice := opsToOpsEngineer(ops)
	c.IndentedJSON(http.StatusOK, devops)

}

func getEngineer(c *gin.Context) {
	//engineer_slice := mapToSlice(engineers)
	c.IndentedJSON(http.StatusOK, engineers)
}

func getDev(c *gin.Context) {
	//dev_slice := devListConversion(developers)
	c.IndentedJSON(http.StatusOK, developers)
}

func getOp(c *gin.Context) {
	//ops_slice := opsListConversion(operations)
	c.IndentedJSON(http.StatusOK, operations)
}

func getDevOps(c *gin.Context) {
	//devops_slice := devopsListConversion(developer_operations)
	c.IndentedJSON(http.StatusOK, developer_operations)
}
