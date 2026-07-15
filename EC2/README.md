# 🚀 Project 01 – Launching My First Amazon EC2 Instance

## 📌 Project Information

| Item               | Details                                |
| ------------------ | -------------------------------------- |
| **Project Name**   | Launching My First Amazon EC2 Instance |
| **Project Status** | ✅ Completed                           |
| **Difficulty**     | ⭐ Beginner                            |
| **Estimated Time** | *45 Minutes*                           |
| **Date Completed** | *15 July 2026*                         |
| **AWS Region**     | *us-east-1 – N. Virgina*               |

---

# 📖 Project Overview

This project marks the beginning of my AWS Cloud Journey.

The objective of this project was to launch my first Amazon EC2 instance, understand the complete deployment workflow, and gain practical experience with AWS compute services.

Rather than simply following a tutorial, I focused on understanding why each AWS service exists, how they work together, and how they relate to technologies I already use on my homelab.

This project serves as the foundation for future cloud projects involving networking, storage, security, automation, and hybrid cloud architectures.

---

# 🎯 Project Objective

Successfully deployed a Linux EC2 instance in AWS, configure secure remote access using SSH, running a Web server and understand the AWS resources required to run a virtual machine in the cloud.

---

# 🛠 AWS Services Used

| AWS Service      | Purpose                                           |
| ---------------- | ------------------------------------------------- |
| Amazon EC2       | Virtual Machine (Compute)                         |
| Amazon EBS       | Persistent Storage                                |
| Security Group   | Virtual Stateful Firewall                         |
| Key Pair         | Secure SSH Authentication                         |
| Amazon VPC       | Network where the EC2 instance is deployed        |
| Internet Gateway | Allows internet connectivity for public resources |

---

# 🧠 Skills Practiced

* AWS Management Console
* Amazon EC2
* Linux Server Deployment
* Amazon Machine Images (AMI)
* Instance Types
* Security Groups
* Key Pair Authentication
* SSH
* Public & Private IP Addressing
* Basic AWS Networking

---

# 🏗 Architecture

```text
                     Internet
                         │
                         │
                 Internet Gateway
                         │
                  Amazon VPC
                         │
                  Public Subnet
                         │
                 Security Group
                         │
                Amazon EC2 Instance
                         │
                   Amazon EBS Volume
```

---

# 🔧 Configuration Details

## Operating System

Ubuntu Server 24.04 LTS *(or your chosen AMI)*

---

## Instance Type

t3.micro *(Free Tier Eligible)*

---

## Authentication

AWS Key Pair (.pem)

---

## Storage

10 GB gp3 Amazon EBS

---

## Network

VPC: Default VPC

Subnet: Default Public Subnet

Public IPv4: Enabled

---

## User Data

```
#!/bin/bash

# updating ubuntu packages
apt update -y

# upgrading ubuntu packages and dependencies 
apt upgrade -y 

# installing, and starting a nginx server
apt install nginx -y

systemctl start nginx 

systemctl enable nginx
```

---

## Security Group Rules

| Type                   | Protocol | Port | Source               |
| ---------------------- | -------- | ---- | -------------------- |
| SSH                    | TCP      | 22   | Anywhere (0.0.0.0/0) |
| HTTP                   | TCP      | 80   | Anywhere (0.0.0.0/0) |

---

# 🚀 Deployment Process

The following high-level steps were performed:

1. Logged into the AWS Management Console.
2. Opened the EC2 Dashboard.
3. Clicked **Launch Instance**.
4. Selected the Ubuntu Server AMI.
5. Chose the t3.micro instance type.
6. Created a new SSH Key Pair.
7. Configured the Security Group.
8. Configured storage.
9. Configured User Data.
9. Launched the EC2 instance.
10. Verified the instance reached the **Running** state.
11. Connected to the instance using SSH.
12. Run test a webpage.

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

## Challenge 1

**Web page wasn't loading**

After the initial boot of the EC2 instance, I tried to open/launch the Nginx landing page using the given public IP, but wasn't redirected to the page.

**Cause**

I quickly realise that I was using *Brave* Browser and immediatly knew the issue. It was redirecting the page in *HTTPS* by default rather *HTTP*.

**Resolution**

I switched to another browser *(Firefox)*, and it redirected to the Nginx landing page without any issue. After that I even tried launcing the web page in *Brave with HTTP* connection and it worked immedately.


---

# 📚 Key Concepts Learned

During this project I learned:

* What Amazon EC2 is.
* The purpose of an Amazon Machine Image (AMI).
* The difference between an AMI and a running EC2 instance.
* How Security Groups control network access.
* Page and Browser Security.
* Why Key Pairs are used instead of passwords.
* The relationship between EC2, VPC, Security Groups, and EBS.
* Basic SSH connectivity.
* User Data configuration.

---

# 💡 Lessons Learned

This project helped me understand that cloud infrastructure is built using many of the same concepts found in traditional on-premises environments.

Although AWS introduces its own terminology and managed services, the underlying principles of compute, networking, storage, and security remain familiar.

Building the environment myself reinforced the concepts far more effectively than reading documentation alone.

---

# 🔄 Future Improvements

Possible enhancements include:

* Attach an additional EBS volume.
* Assign an Elastic IP.
* Install Docker.
* Host a simple web application.
* Configure HTTPS.
* Create an AMI from the instance.
* Automate deployment using Infrastructure as Code (CloudFormation or Terraform).

---

# 📚 References

* AWS Official Documentation
* AWS Cloud Practitioner Learning Material
* AWS Free Tier - Skill Builder
* Personal Hands-on Practice

---

# 📝 Personal Reflection

### What went well?

I successfully launched my first EC2 instance and connected to it using SSH. Understanding the relationship between EC2, Security Groups, and EBS became much clearer after completing the deployment.

---

### What challenged me?

Initially, I confused the with the Security Groups and route spent time understanding how Security Groups differ from traditional firewalls.

---

### What did I discover myself?

One thing I knew and had to configure earlier during the creation of the instance was *User Data* bash script to automate tasks such as installing software or configuring settings right after the instance starts. 

I already knew that the EC2 instance doesn't launch with updated ubuntu packages and Nginx pre-installed and even it reset every time an instance is being rebooted. So I had to make sure that whenever an instance reboot's, all the necessary packages and dependencies should be up-to-date, installed and up-and-running state.

---

### What is my next project?

* Amazon S3 Static Website Hosting
* VPC Fundamentals
* IAM User Management
* Hybrid AWS + Homelab VPN

---

# ✅ Project Summary

This project provided my first practical experience with AWS infrastructure and established a strong foundation for future cloud projects.

By completing this project, I gained hands-on experience with compute resources, networking, storage, and secure remote administration while also improving my ability to document technical work in a structured and professional manner.

This documentation serves as both a learning record and a portfolio artifact demonstrating practical AWS experience.
