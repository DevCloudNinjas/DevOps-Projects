const rawQuizdown = `
---
shuffleAnswers: true
shuffleQuestions: true
---

# What is an S3 bucket?

1. [x] A storage container
	> Good. While it is capable of much more, an S3 bucket, at its core, is a storage container
1. [ ] A runtime host for an app (ie it holds a web server)
	> While a bucket has the ability to host a static web server, this is not all that it is
1. [ ] A runtime instance (it is the web server)
	> Not quite, a bucket can host a web server, but that isn't all that it does
1. [ ] A set of web traffic rules and permissions
	> While a bucket does need these rules, it is not the actual rules themselves

# Long-term storage that is used regularly should be stored in what kind of storage class?

1. [x] Standard
	> Good. Storage that is used frequently should be stored in a Standard storage class
1. [ ] Standard Infrequent Access
	> Not quite. Revisit the [S3 video](https://youtu.be/77lMCiiMilo) if you are confused
1. [ ] Glacier
	> Not quite. Revisit the [S3 video](https://youtu.be/77lMCiiMilo) if you are confused
1. [ ] Frequent Use
	> This is not a real AWS storage class type. Revisit the [S3 video](https://youtu.be/77lMCiiMilo) if you are confused

# Long-term storage that is not used regularly should be stored in what kind of storage class?

1. [ ] Standard
	> Not quite. Revisit the [S3 video](https://youtu.be/77lMCiiMilo) if you are confused
1. [x] Standard Infrequent Access
	> Good. Storage that isn't accessed much should be stored in a Standard Infrequent Access storage class
1. [ ] Glacier
	> Not quite. Revisit the [S3 video](https://youtu.be/77lMCiiMilo) if you are confused
1. [ ] Frequent Use
	> This is not a real AWS storage class type. Revisit the [S3 video](https://youtu.be/77lMCiiMilo) if you are confused

# Long-term storage that is archived (not accessed at all) should be stored in what kind of storage class?

1. [ ] Standard
	> Not quite. Revisit the [S3 video](https://youtu.be/77lMCiiMilo) if you are confused
1. [ ] Standard Infrequent Access
	> Not quite. Revisit the [S3 video](https://youtu.be/77lMCiiMilo) if you are confused
1. [x] Glacier
	> Good. Archived storage should be stored in a Glacier storage class
1. [ ] Frequent Use
	> This is not a real AWS storage class type. Revisit the [S3 video](https://youtu.be/77lMCiiMilo) if you are confused

# True or False: Once you define a storage class type for a bucket, you cannot change it

1. [ ] True
	> Actually, there are a few different ways that you can change a bucket's storage class. Revisit the [S3 video](https://youtu.be/77lMCiiMilo) if you are confused
1. [x] False
	> Good. You can either manually change it, or you can configure a lifecycle policy that will automatically move your storage to the most appropriate storage class

# How does S3 ensure the safety and durability of your data? Select all that apply.<br>For more information about various features, please read the [What is Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) documentation.

- [x] It makes copies of your data and stores them in several different facilities
	> Good. S3 stores your data in multiple facilities, and multiple machines within each facility
- [x] It stores every version of your data in the bucket, instead of overwriting
	> Good. This allows for version rollback if needed
- [x] Buckets have automatic error checking
	> Good. S3 calculates checksums on all network traffic to detect corruption of data packets when storing or retrieving data
- [x] Buckets have automatic self healing
	> Good. This is unlike most storage solutions out there, which is another reason why S3 is so dominant
- [ ] S3 automatically deletes old verisons of storage, reducing data clutter and risk of corruption
	> Incorrect. S3 actually saves all versions of your storage in case you need to roll back.

# How does S3 ensure the security of your data? Select all that apply.<br>For more information, please read the [Access Management and Security](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#S3Features) section of the S3 features documentation.

- [x] Identity and Access Management (IAM)
	> Good. IAM roles dictate who can create/interact with objects in a service account
- [x] Access Control Lists (ACL) 
	> Good. ACLs grant access permissions to specific objects in a service account
- [x] Bucket Policies
	> Good. Bucket Policies add or deny permissions to objects within the bucket
- [x] Query String Authentication
	> Good. QSA allows buckets to be securely shared through URLs that expire after a predefined time
- [x] Encryption of data during transfer and while it's at rest
	> Good. S3 offers full end-to-end encryption to help ensure your data's safety
- [ ] Two-Factor Authentication
	> Incorrect. You can configure your AWS account to support 2FA, but S3 utilizes other authentication methods


`;

export { rawQuizdown }