# 🚀 Project 02 – S3 Bucket and Hosting

## 📌 Project Information

| Item               | Details                                |
| ------------------ | -------------------------------------- |
| **Project Name**   | S3 Bucket and Hosting                  |
| **Project Status** | ✅ Completed                           |
| **Difficulty**     | ⭐ Beginner                            |
| **Estimated Time** | *10 Minutes*                           |
| **Date Completed** | *16 July 2026*                         |
| **AWS Region**     | *us-east-1 – N. Virgina*               |

---

# 📖 Project Overview

The objective of this project was to create an Amazon S3 Bucket and Host a static website. Understanding how bucket and object work's, the access permission and policy.

---

# 🎯 Project Objective

Successfully deployed an Amazon S3 Bucket and Hosted a static website, configure bucket policies and permission's for allowing public traffic to access static website.

---

# 🛠 AWS Services Used

| AWS Service      | Purpose                                           |
| ---------------- | ------------------------------------------------- |
| Amazon S3        | Store object in a bucket                          |
| Static website hosting   | Serve static content hosting           |
| Bucket Policy    | Provides access to the objects stored in the bucket and allow pulic access of the website                 |

---

# 🧠 Skills Practiced

* AWS Management Console
* Amazon S3
* Static web hosting

---

# 🏗 Architecture

```text
                    S3 Bucket
                         │
                         │
                    Object
                         │
                    Bucket Policy
                         │
                    Static website hosting
                         │
                    Public endpoint access
                         │
```

---

# 🔧 Configuration Details

## Bucket policy

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "sillyCarWebsite",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::silly-car-bucket/*"
        }
    ]
}
```
---

# 🚀 Deployment Process

The following steps were performed:

1. Logged into the AWS Management Console.
2. Opened the S3 Dashboard.
3. Clicked **Create bucket**.
4. Selected the Bucket type as *(General purpose)*.
5. Enter Bucket name -> **silly-car-bucket**.
6. Kept **Object Ownership** as *ACLs disabled*.
7. Unchecked the *Block all public access* to enable public access.
8. After creating the bucket -> Upload *(to store object)*.
9. Select files and select upload.
9. In Properties, at the bottom -> Edit **Static website hosting**.
10. Enable static hosting and specify index document(*index.html*) and error document (*error.html*) and save changes.
11. After enabling Static website hosting a Bucket website endpoint should appear. e.g. [http://bucket-name.s3-website-region-1.amazonaws.com]
12. In Permission tab Edit **Bucket policy**. Define bucket policy in json format.
13. Click on the Bucket website endpoint/URL. *(Properties -> Static website hosting)*. It should redirect to the index.html / Landing page.

---

# 📸 Screenshots

* EC2 Dashboard
    <img src="screenshots/EC2 Dashboard.png" alt="EC2-Dashboard">
* Launch Instance Configuration
    <img src="screenshots/Launch EC-2 Instance - 1.png" alt="EC-2-config">
    <img src="screenshots/Launch EC-2 Instance - 2.png" alt="EC-2-config">
* Running EC2 Instance
    <img src="screenshots/AWS web SSH-1.png" alt="running">
    <img src="screenshots/AWS web SSH-2.png" alt="running">
    <img src="screenshots/AWS web SSH-3.png" alt="running">
* User Data
    <img src="screenshots/User Data - Script.png" alt="user-data">
* Security Group Rules
    <img src="screenshots/Security Group.png" alt="security-Group">
* SSH Connection
    <img src="screenshots/CMD SSH-1.png" alt="SSH">
    <img src="screenshots/CMD SSH-2.png" alt="SSH">
* Hosted Webpage
    <img src="screenshots/Web page.png" alt="Web">

*Note : I deliberately redacted those IP's and certain ID's for security reasons*

---

# ⚠ Challenges Encountered

## Challenge 

**403 - Forbidden**

The first error that occured was 403 forbidden. I spent 30 mins rechecking the bucket permission and properties.

**Cause**

I didn't knew that you have to define a bucket policy for accessing the object inside the bucket. I believed that simply unchecking *Block all public access* would allow public access to bucket, objects and Static website.

**Resolution**

After a quick prompt in chatGPT I realised the mistake and defined the bucket policy in permissions tab.


## Challenge 2

**404 Cat not found**

After applying Bucket policy there was a new challenge. 404 - Cat not found 😿.

**Cause**

This error was a familiar one. I quickly knew what mistake were made that I have drag and dropped the entire folder, which did not put the *index.html* in the Bucket's root directory. 

**Resolution**

I simply moved the *index.html* into the root directory of the bucket and all other files at there appropriate location, So that no other error can occur. 

---

# 📚 Key Concepts Learned

During this project I learned:

* S3 Buckets and Object.
* How file strucutre/hierarchy inside Amazon S3 works.
* The need to define a bucket policy.

---

# 💡 Lessons Learned

This project helped me understand that what is a S3 bucket. How it store's object and the hierarchy of S3 bucket and object.

Main lesson that I learned here is the need to have appropriate access of an object, permission and policy.

Amazon S3 also act as serverless Website hosting option for static website.

---

# 🔄 Future Improvements

Possible enhancements include:

* Implementing lifecycle policies to automatically transition data to cheaper storage classes.
* Object access as per "principle-of-the-least-privilege".

---

# 📚 References

* AWS Official Documentation
* AWS Cloud Practitioner Learning Material
* AWS Free Tier - Skill Builder
* Personal Hands-on Practice
* Amazon S3 Documentation
