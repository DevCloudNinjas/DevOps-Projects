package main

import (
	"bytes"
	"encoding/json"
	"github.com/gin-gonic/gin"
	"github.com/devcloudninjas/devops-bootcamp/examples/ch7/devops-resources"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
)

// test email validation
type emailTest struct {
	description string
	email       string
	expected    bool
}

/******* structs request testing *******/
type requestEngineerTest struct {
	description  string
	testEngineer devops_resource.Engineer
	expected     int
}

type requestDevTest struct {
	description string
	testDev     devops_resource.Dev
	expected    int
}

type requestOpTest struct {
	description string
	testOp      devops_resource.Ops
	expected    int
}

type requestDevOpsTest struct {
	description string
	testDev     devops_resource.DevOps
	expected    int
}

/********************************************/

var verifyEmailTests = []emailTest{
	emailTest{"simple valid email format", "bob@bob.com", true},
	emailTest{"valid email with extended domain name", "b0b123@clever.ask.who", true},
	emailTest{"special characters in username", "bob#@bob.com", false},
	emailTest{"no specificied domain name", "bob@bob", false},
	emailTest{"empty string for email", "", false},
}

/******* Slices of Test Cases for Engineer Request *******/
var verifyPostEngineer = []requestEngineerTest{
	requestEngineerTest{"contains client side Id field", devops_resource.Engineer{Name: "Bobs Burgers", Id: getRandId(5), Email: "bob@gmail.com"}, http.StatusCreated},
	requestEngineerTest{"no client side Name field", devops_resource.Engineer{Email: "bob@gmail.com"}, http.StatusBadRequest},
	requestEngineerTest{"no client side Email field", devops_resource.Engineer{Name: "Bobs Burgers"}, http.StatusBadRequest},
	requestEngineerTest{"different engineer", devops_resource.Engineer{Name: "Steven Mendez", Email: "Min3craftSt3v3@gmail.com"}, http.StatusCreated},
	requestEngineerTest{"duplicate engineer", devops_resource.Engineer{Name: "Bobs Burgers", Email: "bob@gmail.com"}, http.StatusBadRequest},
	requestEngineerTest{"client side JSON object with empty fields", devops_resource.Engineer{Name: "", Id: "", Email: ""}, http.StatusBadRequest},
}

var verifyPutEngineer = []requestEngineerTest{
	//Created with client side id TODO: fix where id cannot be created via client side
	requestEngineerTest{"Should update name and email of id 1 engineer", devops_resource.Engineer{Name: "Not Bob", Id: "1", Email: "notbob@gmail.com"}, http.StatusOK},
	requestEngineerTest{"No id", devops_resource.Engineer{Name: "Not Bob", Email: "notbob@gmail.com"}, http.StatusBadRequest},
}

var verifyDeleteEngineer = []requestEngineerTest{
	requestEngineerTest{"should delete nothing and fail", devops_resource.Engineer{Name: "failed", Id: "40"}, http.StatusBadRequest},
	requestEngineerTest{"should delete nothing and fail since no id", devops_resource.Engineer{Name: "NoId"}, http.StatusBadRequest},
	requestEngineerTest{"should delete test engineer and pass", devops_resource.Engineer{Id: "5"}, http.StatusOK},
	requestEngineerTest{"duplicate this should fail", devops_resource.Engineer{Id: "5"}, http.StatusBadRequest},
}

/********************************************/

/******* Slices of Test Cases for Developer Resource Request *******/
var verifyPostDev = []requestDevTest{
	requestDevTest{"simple developer resource creation", devops_resource.Dev{Name: "dev_ferrets"}, http.StatusCreated},
	requestDevTest{"no client side Name field", devops_resource.Dev{}, http.StatusBadRequest},
	requestDevTest{"different developer resource", devops_resource.Dev{Name: "dev_bengal"}, http.StatusCreated},
	requestDevTest{"duplicate developer resource", devops_resource.Dev{Name: "dev_ferrets"}, http.StatusBadRequest},
	requestDevTest{"client side JSON object with empty fields", devops_resource.Dev{Name: ""}, http.StatusBadRequest},
}

var verifyPutDev = []requestDevTest{
	//Created with client side id TODO: fix where id cannot be created via client side
	requestDevTest{"should update name id 2 developer resource", devops_resource.Dev{Name: "notferrets", Id: "2"}, http.StatusOK},
	requestDevTest{"No id", devops_resource.Dev{Name: "dev_notferrets"}, http.StatusBadRequest},
}

var verifyDeleteDev = []requestDevTest{
	requestDevTest{"should delete nothing and fail", devops_resource.Dev{Name: "failed", Id: "40"}, http.StatusBadRequest},
	requestDevTest{"should delete nothing and fail since no id", devops_resource.Dev{Name: "NoId"}, http.StatusBadRequest},
	requestDevTest{"should delete test developer resource and pass", devops_resource.Dev{Id: "4"}, http.StatusOK},
	requestDevTest{"duplicate this should fail", devops_resource.Dev{Id: "4"}, http.StatusBadRequest},
}

/********************************************/

/******* Slices of Test Cases for Operations Resource Request *******/
var verifyPostOp = []requestOpTest{
	requestOpTest{"simple operation resource creation", devops_resource.Ops{Name: "op_ferrets"}, http.StatusCreated},
	requestOpTest{"no client side Name field", devops_resource.Ops{}, http.StatusBadRequest},
	requestOpTest{"different operation resource", devops_resource.Ops{Name: "op_bengal"}, http.StatusCreated},
	requestOpTest{"duplicate operation resource", devops_resource.Ops{Name: "op_ferrets"}, http.StatusBadRequest},
	requestOpTest{"client side JSON object with empty fields", devops_resource.Ops{Name: ""}, http.StatusBadRequest},
}

var verifyPutOp = []requestOpTest{
	//Created with client side id TODO: fix where id cannot be created via client side
	requestOpTest{"should update name id 2 operation resource", devops_resource.Ops{Name: "op_notferrets", Id: "2"}, http.StatusOK},
	requestOpTest{"No id", devops_resource.Ops{Name: "op_notferrets"}, http.StatusBadRequest},
}

var verifyDeleteOp = []requestOpTest{
	requestOpTest{"should delete nothing and fail", devops_resource.Ops{Name: "failed", Id: "40"}, http.StatusBadRequest},
	requestOpTest{"should delete nothing and fail since no id", devops_resource.Ops{Name: "NoId"}, http.StatusBadRequest},
	requestOpTest{"should delete test operation resource and pass", devops_resource.Ops{Id: "2"}, http.StatusOK},
	requestOpTest{"duplicate this should fail", devops_resource.Ops{Id: "2"}, http.StatusBadRequest},
}

/********************************************/

func TestVerifyEmail(t *testing.T) {
	for _, test := range verifyEmailTests {
		result := verifyEmail(test.email)
		if result != test.expected {
			t.Errorf("\nTest: %s\nEmail: %s\nExpected: %t, Received: %t", test.description, test.email, test.expected, result)
		}
	}
}

/******* Engineer Mock Requests *******/
func mockJsonPostEngineer(c *gin.Context, content devops_resource.Engineer) {
	c.Request.Method = "POST"
	c.Request.Header.Set("Content-Type", "application/json")
	jsonBytes, err := json.Marshal(content)
	if err != nil {
		panic(err)
	}

	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonBytes))
}

func mockJsonPutEngineer(c *gin.Context, content devops_resource.Engineer) {
	c.Request.Method = "PUT"
	c.Request.Header.Set("Content-Type", "application/json")
	c.Params = []gin.Param{gin.Param{Key: "id", Value: content.Id}}

	jsonBytes, err := json.Marshal(content)
	if err != nil {
		panic(err)
	}

	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonBytes))
}

func mockJsonDeleteEngineer(c *gin.Context, content devops_resource.Engineer) {
	c.Request.Method = "DELETE"
	c.Request.Header.Set("Content-Type", "application/json")
	c.Params = []gin.Param{gin.Param{Key: "id", Value: content.Id}}

	jsonBytes, err := json.Marshal(content)
	if err != nil {
		panic(err)
	}

	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonBytes))
}

/********************************************/

/******* Dev Mock Requests *******/
func mockJsonPostDev(c *gin.Context, content devops_resource.Dev) {
	c.Request.Method = "POST"
	c.Request.Header.Set("Content-Type", "application/json")
	jsonBytes, err := json.Marshal(content)
	if err != nil {
		panic(err)
	}

	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonBytes))
}

func mockJsonPutDev(c *gin.Context, content devops_resource.Dev) {
	c.Request.Method = "PUT"
	c.Request.Header.Set("Content-Type", "application/json")
	c.Params = []gin.Param{gin.Param{Key: "id", Value: content.Id}}

	jsonBytes, err := json.Marshal(content)
	if err != nil {
		panic(err)
	}

	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonBytes))
}

func mockJsonDeleteDev(c *gin.Context, content devops_resource.Dev) {
	c.Request.Method = "DELETE"
	c.Request.Header.Set("Content-Type", "application/json")
	c.Params = []gin.Param{gin.Param{Key: "id", Value: content.Id}}

	jsonBytes, err := json.Marshal(content)
	if err != nil {
		panic(err)
	}

	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonBytes))
}

/********************************************/

/******* Op Mock Requests *******/
func mockJsonPostOp(c *gin.Context, content devops_resource.Ops) {
	c.Request.Method = "POST"
	c.Request.Header.Set("Content-Type", "application/json")
	jsonBytes, err := json.Marshal(content)
	if err != nil {
		panic(err)
	}

	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonBytes))
}

func mockJsonPutOp(c *gin.Context, content devops_resource.Ops) {
	c.Request.Method = "PUT"
	c.Request.Header.Set("Content-Type", "application/json")
	c.Params = []gin.Param{gin.Param{Key: "id", Value: content.Id}}

	jsonBytes, err := json.Marshal(content)
	if err != nil {
		panic(err)
	}

	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonBytes))
}

func mockJsonDeleteOp(c *gin.Context, content devops_resource.Ops) {
	c.Request.Method = "DELETE"
	c.Request.Header.Set("Content-Type", "application/json")
	c.Params = []gin.Param{gin.Param{Key: "id", Value: content.Id}}

	jsonBytes, err := json.Marshal(content)
	if err != nil {
		panic(err)
	}

	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonBytes))
}

/********************************************/

/******* Test Runs for Engineer Requests *******/
func TestPostEngineer(t *testing.T) {
	var w *httptest.ResponseRecorder
	var c *gin.Context

	for _, test := range verifyPostEngineer {
		w = httptest.NewRecorder()
		c, _ = gin.CreateTestContext(w)
		c.Request = &http.Request{
			Header: make(http.Header),
		}
		mockJsonPostEngineer(c, test.testEngineer)
		postEngineer(c)
		if test.expected != w.Code {
			t.Errorf("\nTest: %s\nExpected: Status Code %d, Received: Status Code %d", test.description, test.expected, w.Code)
		}
	}
	engineers = nil
}

func TestPutEngineer(t *testing.T) {
	var w *httptest.ResponseRecorder
	var c *gin.Context
	engineers = append(engineers, &devops_resource.Engineer{Name: "Bob", Id: "1", Email: "bob@gmail.com"})

	for _, test := range verifyPutEngineer {
		w = httptest.NewRecorder()
		c, _ = gin.CreateTestContext(w)
		c.Request = &http.Request{
			Header: make(http.Header),
		}
		mockJsonPutEngineer(c, test.testEngineer)
		putEngineer(c)
		if test.expected != w.Code {
			t.Errorf("\nTest: %s\nExpected: Status Code %d, Received: Status Code %d", test.description, test.expected, w.Code)
		}
	}
	engineers = nil
}

func TestDeleteRequestEngineer(t *testing.T) {
	var w *httptest.ResponseRecorder
	var c *gin.Context
	engineers = append(engineers, &devops_resource.Engineer{Name: "Bob", Id: "5", Email: "bob@gmail.com"})

	for _, test := range verifyDeleteEngineer {
		w = httptest.NewRecorder()
		c, _ = gin.CreateTestContext(w)
		c.Request = &http.Request{
			Header: make(http.Header),
		}
		mockJsonDeleteEngineer(c, test.testEngineer)
		deleteRequestEngineer(c)
		if test.expected != w.Code {
			t.Errorf("\nTest: %s\nExpected: Status Code %d, Received: Status Code %d", test.description, test.expected, w.Code)
		}
	}
	engineers = nil
}

/********************************************/

/******* Test Runs for Developer Resource Requests *******/
func TestPostDev(t *testing.T) {
	var w *httptest.ResponseRecorder
	var c *gin.Context

	for _, test := range verifyPostDev {
		w = httptest.NewRecorder()
		c, _ = gin.CreateTestContext(w)
		c.Request = &http.Request{
			Header: make(http.Header),
		}
		mockJsonPostDev(c, test.testDev)
		postDev(c)
		if test.expected != w.Code {
			t.Errorf("\nTest: %s\nExpected: Status Code %d, Received: Status Code %d", test.description, test.expected, w.Code)
		}
	}
	developers = nil
}

func TestPutDev(t *testing.T) {
	var w *httptest.ResponseRecorder
	var c *gin.Context
	developers = append(developers, &devops_resource.Dev{Name: "ferrets", Id: "2"})

	for _, test := range verifyPutDev {
		w = httptest.NewRecorder()
		c, _ = gin.CreateTestContext(w)
		c.Request = &http.Request{
			Header: make(http.Header),
		}
		mockJsonPutDev(c, test.testDev)
		putDev(c)
		if test.expected != w.Code {
			t.Errorf("\nTest: %s\nExpected: Status Code %d, Received: Status Code %d", test.description, test.expected, w.Code)
		}
	}
	developers = nil
}

func TestDeleteRequestDev(t *testing.T) {
	var w *httptest.ResponseRecorder
	var c *gin.Context
	developers = append(developers, &devops_resource.Dev{Name: "ferrets", Id: "4"})

	for _, test := range verifyDeleteDev {
		w = httptest.NewRecorder()
		c, _ = gin.CreateTestContext(w)
		c.Request = &http.Request{
			Header: make(http.Header),
		}
		mockJsonDeleteDev(c, test.testDev)
		deleteRequestDev(c)
		if test.expected != w.Code {
			t.Errorf("\nTest: %s\nExpected: Status Code %d, Received: Status Code %d", test.description, test.expected, w.Code)
		}
	}
	developers = nil
}

/********************************************/

/******* Test Runs for Operation Resource Requests *******/
func TestPostOp(t *testing.T) {
	var w *httptest.ResponseRecorder
	var c *gin.Context

	for _, test := range verifyPostOp {
		w = httptest.NewRecorder()
		c, _ = gin.CreateTestContext(w)
		c.Request = &http.Request{
			Header: make(http.Header),
		}
		mockJsonPostOp(c, test.testOp)
		postOp(c)
		if test.expected != w.Code {
			t.Errorf("\nTest: %s\nExpected: Status Code %d, Received: Status Code %d", test.description, test.expected, w.Code)
		}
	}
	operations = nil
}

func TestPutOp(t *testing.T) {
	var w *httptest.ResponseRecorder
	var c *gin.Context
	operations = append(operations, &devops_resource.Ops{Name: "ferrets", Id: "2"})

	for _, test := range verifyPutOp {
		w = httptest.NewRecorder()
		c, _ = gin.CreateTestContext(w)
		c.Request = &http.Request{
			Header: make(http.Header),
		}
		mockJsonPutOp(c, test.testOp)
		putOp(c)
		if test.expected != w.Code {
			t.Errorf("\nTest: %s\nExpected: Status Code %d, Received: Status Code %d", test.description, test.expected, w.Code)
		}
	}
	operations = nil
}

func TestDeleteRequestOp(t *testing.T) {
	var w *httptest.ResponseRecorder
	var c *gin.Context
	operations = append(operations, &devops_resource.Ops{Name: "ferrets", Id: "2"})

	for _, test := range verifyDeleteOp {
		w = httptest.NewRecorder()
		c, _ = gin.CreateTestContext(w)
		c.Request = &http.Request{
			Header: make(http.Header),
		}
		mockJsonDeleteOp(c, test.testOp)
		deleteRequestOp(c)
		if test.expected != w.Code {
			t.Errorf("\nTest: %s\nExpected: Status Code %d, Received: Status Code %d", test.description, test.expected, w.Code)
		}
	}
	operations = nil
}

/********************************************/

func TestNewEngineer(t *testing.T) {
	result, err := newEngineer("test_engineer", "test@gmail.com")
	if result.Email != "test@gmail.com" || result.Name != "test_engineer" {
		t.Errorf("Expected name %s and email %s were not returned", result.Name, result.Email)
	}
	if err != nil {
		t.Errorf("Expected no errors but one was returned")
	}
}

func TestNewEngineerBadName(t *testing.T) {
	result, err := newEngineer("", "test@gmail.com")
	if err == nil {
		t.Errorf("Expected name %s was not returned", result.Name)
	}
	if result != nil {
		t.Errorf("Expected empty struct but one was not returned")
	}
}

func TestNewDev(t *testing.T) {

	result, err := newDev(devops_resource.Dev{Name: "test_devs"})
	if result.Name != "test_devs" {
		t.Errorf("Expected name %s was not returned", result.Name)
	}
	if err != nil {
		t.Errorf("Expected no errors but one was returned")
	}
}

func TestNewDevBadName(t *testing.T) {
	_, err := newDev(devops_resource.Dev{Name: ""})
	if err == nil {
		t.Errorf("Expected name error but one was not returned")
	}
}

func TestNewOp(t *testing.T) {
	result, err := newOp(devops_resource.Ops{Name: "test_ops"})
	if result.Name != "test_ops" {
		t.Errorf("Expected name %s was not returned", result.Name)
	}
	if err != nil {
		t.Errorf("Expected no errors but one was returned")
	}
}

func TestNewDevOps(t *testing.T) {
	_, err := newDevOps(devops_resource.DevOps{})
	if err != nil {
		t.Errorf("Expected no errors but one was returned")
	}
	//possibly test if maps are empty/initialized
}

func TestDeleteEngineer(t *testing.T) {
	result, _ := newEngineer("test_engineer2", "test@gmail.com")
	delete_result, _ := deleteEngineer(result.Id)
	if delete_result == false {
		t.Errorf("Expected true to be returned but %t was instead'", delete_result)
	}
	_, delete2_error := deleteEngineer(result.Id)
	if delete2_error == nil {
		t.Errorf("Expected error to occur on second delete of same object but nil was returned")
	}
}

/*
func TestDeleteDev(t *testing.T) {

}

func TestDeleteOps(t *testing.T) {

}

func TestDeleteDevOps(t *testing.T) {

}


func TestUpdateEngineer(t *testing.T) {

}

func TestUpdateDev(t *testing.T) {

}
func TestUpdateOps(t *testing.T) {

}

func TestAddOpsTo_DevOps(t *testing.T) {

}
func TestAddDevTo_DevOps(t *testing.T) {

}
func TestAddEngineerTo_Dev(t *testing.T) {

}
func TestAddEngineerTo_Ops(t *testing.T) {

}

func TestDeleteOpsFrom_DevOps(t *testing.T) {

}
func TestDeleteDevFrom_DevOps(t *testing.T) {

}
func TestDeleteEngineerFrom_Dev(t *testing.T) {

}
func TestDeleteEngineerFrom_Ops(t *testing.T) {

}
*/

func TestFindEngineerByName(t *testing.T) {
	newEngineer("bob", "bob@bob.com")
	_, err := findEngineer_by_Name("bob")
	if err != nil {
		t.Errorf("Error: %v", err)
	}
	engineers = nil
}

func TestFindBadEngineerByName(t *testing.T) {
	newEngineer("bob", "bob@gmail")
	_, err := findEngineer_by_Name("bobby")
	if err == nil {
		t.Errorf("Error: Expected Errors, recieved none.")
	}
	engineers = nil
}

func TestFindEngineerByEmail(t *testing.T) {
	newEngineer("bob", "bob@gmail.com")
	_, err := findEngineer_by_Email("bob@gmail.com")
	if err != nil {
		t.Errorf("Error: %v", err)
	}
	engineers = nil
}

func TestFindBadEngineerByEmail(t *testing.T) {
	newEngineer("bob", "bob@gmail")
	_, err := findEngineer_by_Email("bob@bob.com")
	if err == nil {
		t.Errorf("Error: Expected Errors, recieved none.")
	}
	engineers = nil
}

func TestFindDevByName(t *testing.T) {
	newDev(devops_resource.Dev{Name: "dev_ferrets"})
	_, err := findDev_by_Name("dev_ferrets")
	if err != nil {
		t.Errorf("Error: %v", err)
	}
	developers = nil
}

func TestFindBadDevByName(t *testing.T) {
	newDev(devops_resource.Dev{Name: "dev_ferrets"})
	_, err := findDev_by_Name("dev_bengals")
	if err == nil {
		t.Errorf("Error: Expected Errors, recieved none.")
	}
	developers = nil
}

func TestFindOpsByName(t *testing.T) {
	newOp(devops_resource.Ops{Name: "ops_ferrets"})
	_, err := findOps_by_Name("ops_ferrets")
	if err != nil {
		t.Errorf("Error: %v", err)
	}
	operations = nil
}

func TestFindBadOpsByName(t *testing.T) {
	newOp(devops_resource.Ops{Name: "ops_ferrets"})
	_, err := findOps_by_Name("ops_bengals")
	if err == nil {
		t.Errorf("Error: Expected Errors, recieved none.")
	}
	operations = nil
}
