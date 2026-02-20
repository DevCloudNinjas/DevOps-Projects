# Create a CI/CD Pipeline for Python application in **Azure DevOps** with integrate with **Azure Repos** with pipeline script of deployment and test stages and finally push to **Azure Artifacts**

![ci-cd](https://imgur.com/D1OFqlv.png)

>Creating a CI/CD pipeline for a Python application in Azure DevOps, integrating it with Azure Repos, and including stages for deployment, testing, and publishing to Azure Artifacts can be done with a YAML pipeline script. Here's a step-by-step guide:

**Prerequisites:**
1. An Azure DevOps account and a project.
2. A Python application hosted in an Azure Repos Git repository.
3. An Azure Artifacts feed for publishing your Python packages.

**Step 1: Set Up Your Repository**
Ensure your Python application is hosted in an Azure Repos Git repository. Your repository should contain the application code, a `requirements.txt` file listing project dependencies, a script to run your application, and unit tests.

**Step 2: Create an Azure DevOps Pipeline**

1. Log in to your Azure DevOps account.

2. Go to your Azure DevOps project.

3. Click on "Pipelines" in the left navigation menu.

4. Click on the "New Pipeline" button.

5. Azure DevOps will guide you through a series of setup steps. Choose "Azure Repos Git" as your code repository source and select your repository.

**Step 3: Configure the Pipeline**

Once the basic pipeline is created, you need to configure it further by adding stages for deployment, testing, and publishing to Azure Artifacts:

```yaml
trigger:
- master  # Set the branch you want to trigger the pipeline on

pr:
- '*'

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Build
  jobs:
  - job: Build
    displayName: 'Build and Test'
    steps:
    - script: |
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        python -m pytest tests/
      displayName: 'Run Tests'

    - script: |
        python setup.py sdist bdist_wheel
      displayName: 'Build Distribution'

    - task: PublishBuildArtifacts@1
      displayName: 'Publish Build Artifacts'
      inputs:
        pathtoPublish: '$(System.DefaultWorkingDirectory)/dist'
        artifactName: 'python-distribution'

- stage: Deploy
  jobs:
  - job: Deploy
    displayName: 'Deploy to Azure Artifacts'
    dependsOn: Build
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.x'
        addToPath: true

    - script: |
        pip install twine
        twine upload --repository-url <Your_Azure_Artifacts_Repo_URL> --skip-existing $(System.DefaultWorkingDirectory)/dist/*
      displayName: 'Publish to Azure Artifacts'
```

In this YAML configuration:

- The pipeline is triggered when changes are pushed to the `master` branch or when pull requests are created (`pr: '*'`).
- It uses an Ubuntu agent (`vmImage: 'ubuntu-latest'`).
- The "Build" stage sets up a Python virtual environment, installs dependencies, runs unit tests using pytest, builds a Python distribution package, and publishes the package as a build artifact.
- The "Deploy" stage installs Twine, a package manager for Python, and uploads the package to Azure Artifacts. Replace `<Your_Azure_Artifacts_Repo_URL>` with the actual URL of your Azure Artifacts feed.

**Step 4: Save and Run the Pipeline**

Save the YAML file and commit it to your Azure Repos Git repository. Azure DevOps will automatically detect changes and run the pipeline.

**Step 5: Monitor and Troubleshoot**

After your pipeline is running, you can monitor its progress, view logs, and troubleshoot any issues using the Azure DevOps interface.

This setup creates a comprehensive CI/CD pipeline for a Python application hosted in Azure Repos, including stages for deployment, testing, and publishing to Azure Artifacts. You can further customize the pipeline to include additional steps, such as code quality checks or deployment to different environments, based on your project's specific requirements.

## By [Harshhaa Reddy](https://www.github.com/NotHarshhaa)
