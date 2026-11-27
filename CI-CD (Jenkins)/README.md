# Jenkins CI/CD Learning

## Purpose

This document records the concepts covered while learning Jenkins and CI/CD. It is a learning record, not a claim that every concept has been understood, deployed or worked with in a production environment.

## Learning context

The learning phase followed an initial study of the Software Development Life Cycle (SDLC), Continuous Integration (CI), and Continuous Delivery/Deployment (CD). The practical goal was to understand CI/CD as an infrastructure and automation tools and its capability that can be applied to cloud and DevOps work.

I have been learning Jenkins CI/CD primarily from YouTube, particularly through [CloudWithVarJosh's](https://github.com/CloudWithVarJosh) -  [**Jenkins CI/CD Basics-to-Production**](https://github.com/CloudWithVarJosh/Jenkins-Basics-To-Production). 

This [17-hour](https://www.youtube.com/watch?v=wj8ELsJ-S5Q) comprehensive course not only provided hands-on experience with Freestyle, Pipeline, and Multibranch Pipeline jobs across local machines, Docker, and AWS EC2 environments but also helped clarify DevOps concepts, resolve doubts, and understand industry best practices through practical, real-world examples, easy-to-understand analogies and diagrams.

## 1. SDLC and CI/CD

### SDLC

The Software Development Life Cycle describes the broad process used to plan, build, test, release, and maintain software. CI/CD automation supports repeatable parts of this lifecycle.

### Continuous Integration (CI)

CI is the practice of frequently integrating changes into a shared codebase and automatically validating those changes. A typical CI workflow can:

1. Retrieve source code from version control.
2. Install required dependencies.
3. Run automated tests.
4. Generate test or coverage reports.
5. Run static analysis and quality checks.
6. Report whether the change passed the defined checks.

### Continuous Delivery and Continuous Deployment

- **Continuous Delivery:** the application is kept in a deployable state; production release may still require a human approval.
- **Continuous Deployment:** changes that pass the required automated checks are automatically released to production.

A pipeline can implement CI without necessarily implementing production deployment. Building and testing an application is not the same as deploying it.

## 2. Jenkins as an automation server

Jenkins is an automation server used to orchestrate repeatable tasks such as builds, tests, analysis, packaging, and deployment.

A useful mental model is that Jenkins is an **automation engine**. It coordinates work; the commands and tools in the pipeline perform the actual tasks.

Examples of tools a pipeline may invoke include Git, Python, Maven, pytest, SonarQube scanners, Docker, shell commands, and deployment tooling.

## 3. Jenkins architecture

### Controller

The Jenkins controller provides the web interface and coordinates jobs and builds. It schedules work and manages configuration, plugins, credentials, and build metadata.

### Agents and executors

Agents provide execution environments for pipeline work. Executors represent the capacity to run builds on an agent.

A small lab may run builds on the controller itself. Larger or more isolated setups can use separate agents. The important operational lesson is that a pipeline runs in the environment assigned to its build, not necessarily in the same environment as an administrator's interactive SSH session.

### Workspace

A workspace is the directory Jenkins allocates for a job's working files. It commonly contains the checked-out repository and generated build artefacts. Different jobs can have different workspaces.

### Environment and PATH

A Jenkins build can run as a different operating-system user and with a different environment/PATH from an interactive login shell. Therefore, a command that works after manually SSH-ing into an EC2 instance may fail in a Jenkins job.

Prefer explicit executable paths or a controlled virtual environment when reproducibility matters. For Python, for example, invoking `.venv/bin/python -m pip` avoids relying on an ambiguous `pip` executable being on PATH.

## 4. Jenkins jobs and pipeline styles

### Freestyle job

A Freestyle project is configured primarily through the Jenkins UI. It is useful for learning job configuration, source checkout, build steps, and post-build actions.

### Pipeline job

A Pipeline job defines a sequence of stages and steps, commonly in a `Jenkinsfile` stored with the source code.

A Declarative Pipeline commonly uses:

- `pipeline` as the top-level block.
- `agent` to select where the pipeline runs.
- `stages` to group the workflow.
- `stage` to name a logical phase.
- `steps` to run commands or Jenkins steps.
- `post` for actions that run after the pipeline or stage, depending on its placement and conditions.

Example skeleton:

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Retrieve source code
            }
        }

        stage('Build') {
            steps {
                // Run build commands
            }
        }

        stage('Test') {
            steps {
                // Run automated tests
            }
        }
    }
}
```

This is an illustrative snippet, not a copy of a particular lab's final Jenkinsfile.

### Multibranch Pipeline

A Multibranch Pipeline job discovers branches in a source-code repository and can run a branch-specific Jenkinsfile for each discovered branch. This is useful when different branches need independent build and validation runs.

It differs from a single Pipeline job that is configured to build one selected branch.

## 5. Jenkinsfile and pipeline design

A Jenkinsfile is a text-based pipeline definition. Keeping it in version control makes the automation reviewable and allows the pipeline to evolve alongside the application.

A pipeline is easier to understand when divided into stages that represent meaningful phases, for example:

1. Checkout
2. Dependency installation
3. Test and coverage
4. Static analysis
5. Quality Gate
6. Image & Container build
7. Deployment or run step
8. Post Actions

Not every pipeline needs every stage. The stages should reflect the actual workflow and its acceptance criteria.

## 6. Plugins, credentials, and integrations

Jenkins plugins add integrations and capabilities. Examples in the learning work included source-control, pipeline, Docker, and SonarQube-related functionality.

Credentials should be stored in Jenkins' credential system and referenced by ID from jobs or Jenkinsfiles. Avoid hardcoding tokens, passwords, or other secrets in source code or logs.

For example, a configured SonarQube server connection and a credential ID can be referenced by a pipeline. The exact plugin and step syntax depends on the installed plugin versions and configuration.

## 7. Jenkins compared with GitHub Actions

Both Jenkins and GitHub Actions can automate CI/CD workflows. They are different execution platforms, but many underlying concepts transfer:

| Concept | Jenkins | GitHub Actions |
|---|---|---|
| Workflow definition | Jenkinsfile | Workflow YAML |
| Execution environment | Controller/agent | Runner |
| Workflow units | Stages and steps | Jobs and steps |
| Secrets | Jenkins Credentials | Repository/environment secrets |
| Extensions | Plugins | Actions |
| Triggering | Webhooks, schedules, manual triggers, etc. | Repository events, schedules, manual triggers, etc. |

### Why Jenkins over GitHub Actions?

The learning decision was to start with Jenkins to develop and understand transferable CI/CD and execution-environment fundamentals, then apply those concepts to GitHub Actions later. Jenkins knowledge is not identical to GitHub Actions syntax, but concepts such as runners/agents, checkout, environment variables, secrets, test execution, artifacts, and deployment remain relevant.

## 8. Important lessons and troubleshooting principles

- A command working in an SSH session does not prove it will work in Jenkins. Check the build user, PATH, working directory, installed tools, and permissions.
- Jenkins shell steps may execute in separate shell processes. Do not assume shell state such as an activated virtual environment persists between separate `sh` steps.
- On `/bin/sh`, `source` may not be available. The POSIX-compatible dot command (`. .venv/bin/activate`) is more portable, although explicitly invoking `.venv/bin/python` is often clearer.
- Prefer `python -m pip` using the intended interpreter rather than assuming `pip` resolves to the correct installation.
- Keep credentials out of repository files and console output.
- A successful build stage does not automatically mean the application has been deployed.
- A Quality Gate only enforces the conditions configured in that gate. It does not automatically fail for every issue visible in the SonarQube dashboard.

## 9. Current learning boundary

The Jenkins course and foundational job types have been completed. I am currently practicing Jenkins pipeline and extending them to automate a Python application workflow that includes SAST, code coverage, SonarQube analysis, a Quality Gate check, and Docker operations including Docker images and artifacts.

Terraform, Ansible, and monitoring/Grafana are future learning areas and not a completed part of this Jenkins learning phase.

## 10. Suggested next learning progression

1. Finish and stabilize the independent Jenkins pipeline.
2. Confirm that tests, coverage, SonarQube analysis, and Quality Gate behaviour are reproducible.
3. Handle credentials and environment configuration safely.
4. Later, connect CI/CD to infrastructure automation and monitoring as separate learning milestones.
5. Incorporate IaC tools such as Terraform and Ansible, followed by monitoring such as Grafana or AWS CloudWatch

---
- *Documentation note: I might update this file in future when a concept is revisited or new capability is actually implemented.*
- *Behind but not outdated: This Documentation work is slightly behind my practical work and projects because I haven't had a chance to keep the documentation up to date. :P*
