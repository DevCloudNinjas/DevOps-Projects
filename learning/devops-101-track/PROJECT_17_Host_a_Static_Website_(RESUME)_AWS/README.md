# Project: Host a Static Website (RESUME) on AWS with S3, Cloud-Front, Route53    

</br>
<kbd align="center"><img src="Images/0.jpg"/></kbd>
</br>

## Pre-requisites:-

* AWS Account
* GitHub Account
* Custom Domain
* Basic Knowledge About CloudFront, S3, Route53, AWS Certificate Manager

### Steps:

#### 1. Create your own Resume/Portfolio Website or Clone the sample repository created for this project.

</br>
<kbd align="center"><img src="Images/1.jpg"/></kbd>
</br>


#### 2. Create a New S3 Bucket & Upload your Resume Website Files.

#### 3. Enable S3 Static Website Hosting Feature

#### 4. Connect your Domain to Route53 by Creating a Hosted Zone.

#### 5. Obtain a SSL Certificate 

#### 6. Create a CloudFront Distribution & Connect it with your S3 Bucket 

#### 7. Set Bucket Policy to Allow Cloudfront to access S3

#### 8. Connect CloudFront to Route53 to redirect Traffic

#### 9. Finally Visit your Website to See the Resume


### Step 1:-
If you have not any Project Please use Below GitHub Repository it contains a Sample Resume Website


Note:Before Proceeding you should have your custom Domain you can buy a new domain or you can get a free  domain from Freenom.com


### Step 2:
Let's Create a new S3 Bucket and upload our Resume Files Go to your AWS Console & Open S3 & click on Create Bucket

</br>
<kbd align="center"><img src="Images/2.jpg"/></kbd>
</br>

Provide Bucket Name & choose Your Region 

</br>
<kbd align="center"><img src="Images/3.jpg"/></kbd>
</br>

For Security reasons block Public Access we are going to use CloudFront for Serve the Website

</br>
<kbd align="center"><img src="Images/4.jpg"/></kbd>
</br>

We are using Server-Side encryption with Amazon S3-Manged  Keys to reduce overhead of key management

After that click on Create Bucket & open your Bucket

Upload your Resume Website Files

</br>
<kbd align="center"><img src="Images/5.jpg"/></kbd>
</br>


Finally Upload your Website Files

</br>
<kbd align="center"><img src="Images/6.jpg"/></kbd>
</br>


You can see I have Successfully Uploaded My Website Files

### Step 3:-

Now Let's Enable S3 Static Website Hosting Feature

Go to your Bucket -> Properties -> Static Website Hosting

as shown in below image edit & enable feature

</br>
<kbd align="center"><img src="Images/7.jpg"/></kbd>
</br>

Provide Your Index Document for me its index.html

After that click on Save Changes.

### Step 4:-

Let's Connect our Domain to Route53

Go to Route53 in AWS -> Hosted Zone 

Create a new Hosted Zone

</br>
<kbd align="center"><img src="Images/8.jpg"/></kbd>
</br>


Provide Your Domain Name & Click on Create Hosted Zone

Now Let's Connect our domain to Route53

Open your Hosted Zone You can see 4 NS Records , we

need to add that in our Domain Fields.

Go to your Domain Management & add 4 NameServers

as shown in the below image

</br>
<kbd align="center"><img src="Images/9.jpg"/></kbd>
</br>


You have successfully created your domain to Route53

### Step 5:-

Let's Obtain a SSL Certificate from AWS Certificate Manager

Go to your AWS Console -> Certificate Manager

Click on List Certificates -> Request

You can see below screen click on next

</br>
<kbd align="center"><img src="Images/10.jpg"/></kbd>
</br>


Provide your domain name let all the configurations as it is and click on Request

You can see your Request status as "Pending Validation"

Open that Certificate & click on created records in Route53 as shown in the below image

</br>
<kbd align="center"><img src="Images/12.jpg"/></kbd>
</br>


After that click on Create Records

</br>
<kbd align="center"><img src="Images/13.jpg"/></kbd>
</br>


After few minutes you can see your Certificate status as "Issued"

### Step 6:-

Let's Create a CloudFront distribution with S3 bucket origin and SSL Certificate

Go to your AWS Console -> CloudFront -> Create Distribution

Provide the Origin Domain as your S3 Bucket 

</br>
<kbd align="center"><img src="Images/14.jpg"/></kbd>
</br>


Provide the Origin Access as shown in image & select your Bucket

</br>
<kbd align="center"><img src="Images/20.jpg"/></kbd>
</br>


Provide the Viewer protocol policy as shown in the image as we are going to redirect the traffic to HTTPS

</br>
<kbd align="center"><img src="Images/15.jpg"/></kbd>
</br>


Add your Alternate Domain Name 

</br>
<kbd align="center"><img src="Images/16.jpg"/></kbd>
</br>


Add your SSL Certificate

</br>
<kbd align="center"><img src="Images/17.jpg"/></kbd>
</br>


Finally click on Create Distribution

### Step 7:

Let's Set Bucket Policy to allow cloudfront to access s3

Go to Buckets -> Open the Bucket we have created

Go to Permission -> Edit Bucket Policy

</br>
<kbd align="center"><img src="Images/18.jpg"/></kbd>
</br>


As shown in the image give the same policy edit the provided info as per your bucket and cloudfront distribution

After that click on Save Changes 

### Step 8:

Now Let's Connect our CloudFront to Route53

Go to Route53 -> Hosted Zone -> Open hosted zone that

we have created

After that click on Create Record

Record Type -> A

Alias -> should be enable

Route Traffic to -> Alias to cloudfront distribution

choose distribution that we have created

Finally click on Create Records 

</br>
<kbd align="center"><img src="Images/19.jpg"/></kbd>
</br>


Refer the above Image for Configurations


### Step 9:-

Let's add a error page so that if any error request occurs users should redirect to error page

Go to CloudFront -> Open the CloudFront Distribution that

we have created

Open Error Pages click on Create custom error response

</br>
<kbd align="center"><img src="Images/21.jpg"/></kbd>
</br>


After that click on Save Changes if we anything like

URL/random_string

we can see the error Page

</br>
<kbd align="center"><img src="Images/22.jpg"/></kbd>
</br>


Now you can visit your Website & its Completely hostedby the AWS.



Follow For More Devops: -
https://www.linkedin.com/in/devops-learning
