# DEPLOYING A SIMPLE BOOK REGISTER APPLICATION WITH MEAN STACK IN AWS CLOUD

A MEAN web stack comprises the following components: **MongoDB** which stores and allows to retrieve data, **Express** which makes request to Database for Reads and Writes, **Angular** which handles Client and Server request and **Nodejs** which accepts request and displays results to the end user.
The following steps are taken to deploy a MEAN web stack application:

## STEP 1: Setting up a virtual server in the cloud

To setup a virtual server, I Created a new EC2 Instance of t2.nano family with Ubuntu Server 20.04 LTS (HVM) image from AWS account. After a successful launch of the EC2 instance(ubuntu server), I connected to the EC2 instance from MobaXterm(as a window user) terminal with my private key(.pem file).

## STEP 2: Server Configuration

The following commands are used to configure the ubuntu server:
-	Update ubuntu :`$ sudo apt update`
-	Upgrade ubuntu:`$ sudo apt upgrade`
![](./img/project4/apt%20update%20and%20upgrade.png)

## STEP 3: Installing NodeJS

-	Adding certificates:`$ sudo apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates`
![](./img/project4/adding%20certificates.png)
-	To get the location of Node.js software from Ubuntu repositories :`$ curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash –`
![](./img/project4/installing%20nodejs%20from%20nodeSource.png)
-	Installing NodeJS: `$ sudo apt install –y nodejs`
![](./img/project4/installing%20nodejs.png)

## STEP 4: Installing Mongodb

-	Adding the key used to protect the package:`$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6`
-	Adding the repo where ubuntu will fetch mongodb package to the sources.list file:`$ echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list`
-	Installing the mongodb : `$ sudo apt install -y mongodb`
![](./img/project4/installing%20mongodb.png)
-	Statring the mongodb server: `$ sudo service mongodb start`
-	verifying that the service is up and running: `$ sudo systemctl status mongodb`
-	Install body-parser package which helps in processing JSON files passed in requests to the server: `$ sudo npm install body-parser`
-	Creating a folder called Books moving into it: `$ mkdir Books && cd Books`
-	Initializing npm project in the Books directory: `$ npm init`
![](./img/project4/npm%20init.png)
-	Creating a file called 'server' and opening it in a file editor: `$ vi server`
-	Entering the following codes:
```
var express = require('express');
var bodyParser = require('body-parser');
var app = express();
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());
require('./apps/routes')(app);
app.set('port', 3300);
app.listen(app.get('port'), function() {
    console.log('Server up: http://localhost:' + app.get('port'));
})
```
## Step 5: Installing Express and setting up routes to the server

-	Installing express and mongoose to establish a schema for the database to store data of our book register: `$ sudo npm install express mongoose`
![](./img/project4/instaling%20mongoose%20and%20express.png)
-	Creating a folder called 'apps' in the Books directory and moving into it: `$ mkdir apps && cd apps`
-	Creating a file called 'routes' by opening it in an editor: `$ vi routes` 
-	Entering the following codes:
```
	var Book = require('./models/book');
	module.exports = function(app) {
	  app.get('/book', function(req, res) {
	    Book.find({}, function(err, result) {
	      if ( err ) throw err;
	      res.json(result);
	    });
	  }); 
	  app.post('/book', function(req, res) {
	    var book = new Book( {
	      name:req.body.name,
	      isbn:req.body.isbn,
	      author:req.body.author,
	      pages:req.body.pages
	    });
	    book.save(function(err, result) {
	      if ( err ) throw err;
	      res.json( {
	        message:"Successfully added book",
	        book:result
	      });
	    });
	  });
	  app.delete("/book/:isbn", function(req, res) {
	    Book.findOneAndRemove(req.query, function(err, result) {
	      if ( err ) throw err;
	      res.json( {
	        message: "Successfully deleted the book",
	        book: result
	      });
	    });
	  });
	  var path = require('path');
	  app.get('*', function(req, res) {
	    res.sendfile(path.join(__dirname + '/public', 'index.html'));
	  });
	};
```

-	Creating a folder called 'models' in the app folder and moving into it: '$ mkdir models && cd models'
-	Creating a file called 'books.js' by opening it in an editor: `$ vi books.js`
-	Entering the following codes:
```
	var mongoose = require('mongoose');
	var dbHost = 'mongodb://localhost:27017/test';
	mongoose.connect(dbHost);
	mongoose.connection;
	mongoose.set('debug', true);
	var bookSchema = mongoose.Schema( {
	  name: String,
	  isbn: {type: String, index: true},
	  author: String,
	  pages: Number
	});
	var Book = mongoose.model('Book', bookSchema);
	module.exports = mongoose.model('Book', bookSchema);
 ``` 
## Step 6 – Accessing the routes with AngularJS

-	Changing the directory back to Books directory: `$ cd ../..`
-	Creating a folder called 'public' and moving into it: `$ mkdir public && cd public`
-	Creating a file called 'script.js' by opening it in an editor: `$ vi script.js`
-	Entering the following codes:
```
	var app = angular.module('myApp', []);
	app.controller('myCtrl', function($scope, $http) {
	  $http( {
	    method: 'GET',
	    url: '/book'
	  }).then(function successCallback(response) {
	    $scope.books = response.data;
	  }, function errorCallback(response) {
	    console.log('Error: ' + response);
	  });
	  $scope.del_book = function(book) {
	    $http( {
	      method: 'DELETE',
	      url: '/book/:isbn',
	      params: {'isbn': book.isbn}
	    }).then(function successCallback(response) {
	      console.log(response);
	    }, function errorCallback(response) {
	      console.log('Error: ' + response);
	    });
	  };
	  $scope.add_book = function() {
	    var body = '{ "name": "' + $scope.Name + 
	    '", "isbn": "' + $scope.Isbn +
	    '", "author": "' + $scope.Author + 
	    '", "pages": "' + $scope.Pages + '" }';
	    $http({
	      method: 'POST',
	      url: '/book',
	      data: body
	    }).then(function successCallback(response) {
	      console.log(response);
	    }, function errorCallback(response) {
	      console.log('Error: ' + response);
	    });
	  };
	});
```
-	Creating a file called 'index.html' by opening it in editor: `$ vi index.html`
-	Entering the following codes:
```
	<!doctype html>
	<html ng-app="myApp" ng-controller="myCtrl">
	  <head>
	    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.4/angular.min.js"></script>
	    <script src="script.js"></script>
	  </head>
	  <body>
	    <div>
	      <table>
	        <tr>
	          <td>Name:</td>
	          <td><input type="text" ng-model="Name"></td>
	        </tr>
	        <tr>
	          <td>Isbn:</td>
	          <td><input type="text" ng-model="Isbn"></td>
	        </tr>
	        <tr>
	          <td>Author:</td>
	          <td><input type="text" ng-model="Author"></td>
	        </tr>
	        <tr>
	          <td>Pages:</td>
	          <td><input type="number" ng-model="Pages"></td>
	        </tr>
	      </table>
	      <button ng-click="add_book()">Add</button>
	    </div>
	    <hr>
	    <div>
	      <table>
	        <tr>
	          <th>Name</th>
	          <th>Isbn</th>
	          <th>Author</th>
	          <th>Pages</th>
	
	        </tr>
	        <tr ng-repeat="book in books">
	          <td>{{book.name}}</td>
	          <td>{{book.isbn}}</td>
	          <td>{{book.author}}</td>
	          <td>{{book.pages}}</td>
	
	          <td><input type="button" value="Delete" data-ng-click="del_book(book)"></td>
	        </tr>
	      </table>
	    </div>
	  </body>
	</html>
```
-	Changing the directory back to the books directory: `$ cd ..`
-	Starting the server: `$ node server.js`
![](./img/project4/some%20codes.png)

## STEP 7: Updating the EC2 instance Security Group

-	Configuring the security group of the EC2 instance to be able to listen to port 3300
![](./img/project4/adding%20a%20rule%20to%20the%20security%20group.png)

## FINAL STEP

Opening up my browser and entering my public address with the port number 3300 to access the Book register application:
![](./img/project4/the%20simple%20book%20registrar.png)
