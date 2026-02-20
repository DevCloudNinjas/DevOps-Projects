package main

import (
	"crypto/rand"
	"encoding/base32"
	"regexp"

	"github.com/gin-gonic/gin"
	devops_resource "github.com/DevCloudNinjas/DevOps-Projects/learning/devops-bootcamp/examples/ch7/devops-resources"
)

// Global maps to access our resources by id key
var engineers = make([]*devops_resource.Engineer, 0)
var developers = make([]*devops_resource.Dev, 0)
var operations = make([]*devops_resource.Ops, 0)
var developer_operations = make([]*devops_resource.DevOps, 0)

func verifyEmail(email string) bool {
	result, _ := regexp.MatchString("^[\\w._%+\\-\\/\\]+@[\\w.\\-]+\\.[a-z]{2,4}$", email)
	return result
}

func getRandId(length int) string {
	randomBytes := make([]byte, 32)
	_, err := rand.Read(randomBytes)
	if err != nil {
		panic(err)
	}
	return base32.StdEncoding.EncodeToString(randomBytes)[:length]
}

func main() {
	router := gin.Default()

	//GET routes
	router.GET("/engineers", getEngineer)
	router.GET("/engineers/id/:id", getSpecificEngineerById)
	router.GET("/engineers/name/:name", getSpecificEngineerByName)
	router.GET("/engineers/email/:email", getSpecificEngineerByEmail)
	router.GET("/dev", getDev)
	router.GET("/dev/id/:id", getSpecificDevById)
	router.GET("/dev/name/:name", getSpecificDevByName)
	router.GET("/op", getOp)
	router.GET("/op/id/:id", getSpecificOpsById)
	router.GET("/op/name/:name", getSpecificOpsByName)
	router.GET("/devops", getDevOps)
	router.GET("/devops/:id", getSpecificDevOpsById)

	//POST routes
	router.POST("/engineers", postEngineer)
	router.POST("/dev", postDev)
	router.POST("/op", postOp)
	router.POST("/devops", postDevOps)
	router.POST("/dev/:id", postDevEngineer)
	router.POST("/op/:id", postOpEngineer)
	router.POST("/devops/dev/:id", postDevOpsDev)
	router.POST("/devops/op/:id", postDevOpsOp)

	//PUT routes
	router.PUT("/engineers/:id", putEngineer)
	router.PUT("/dev/:id", putDev)
	router.PUT("/op/:id", putOp)
	router.PUT("/devops/:id", putDevOps)

	//DELETE routes
	router.DELETE("/engineers/:id", deleteRequestEngineer)
	router.DELETE("/dev/:id", deleteRequestDev)
	router.DELETE("/op/:id", deleteRequestOp)
	router.DELETE("/devops/:id", deleteRequestDevOps)

	//runs server
	router.Run(":8080")
}
