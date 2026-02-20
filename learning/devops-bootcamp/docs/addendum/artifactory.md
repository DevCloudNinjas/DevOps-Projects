# Artifactory

![artifactory image](img-addendum/artifactory_light.svg ':size=400px :class=light-mode-img-center :alt= artifactory image; light mode')
![artifactory image](img-addendum/artifactory_dark.svg ':size=400px :class=dark-mode-img-center :alt= artifactory image; dark mode')

## What is Artifactory?

JFrog Artifactory is an enterprise-ready artifact repository. This means that it is used to store built code (artifacts) giving us an easy way to manage different versions of software. The term "enterprise-ready" simply refers to the fact that Artifactory is set up to be integrated with a wide variety CI/CD tools.

Artifactory provides you with the features you need to manage your binary repositories, both through an intuitive UI and with an extensive set of APIs.

The Artifactory UI is divided into four main modules:

**Home**

- The Home module serves as a dashboard where you can easily access general information and commonly used features.

**Artifacts**

- The Artifacts module is used to browse the repositories in your system and search for artifacts using a number of different methods. While browsing through repositories, Artifactory displays useful information and provides you with tools to perform essential actions to manage your repositories.

**Search**

- The Search module is where you can search for Artifacts by name, package type, properties and a variety of additional methods offered by Artifactory.

**Build**

- The Build module displays the Build Browser where you can view all the CI server projects that output their builds to Artifactory.  Here you can drill down to view detailed build information and compare one build to another.

## Installation

1. Download the ZIP file for [Open Source Artifactory](https://jfrog.com/open-source/).
2. Following the [manual installation](https://www.jfrog.com/confluence/display/RTF/Installing+on+Linux+Solaris+or+Mac+OS#InstallingonLinuxSolarisorMacOS-ManualInstallation) instructions and install Artifactory in a new local virtual host or container.
3. Open the Artifactory web interface [http://localhost:8081/artifactory](http://localhost:8081/artifactory) and configure it using the Onboarding Wizard.
4. Create an [Artifactory bootstrap YAML] file and setup a new instance with it. Note: try integrating this into a vagrant provisioner script or part of a Docker image build.

# Deliverable

- Understand the installation and setup process for Artifactory.
- Understand how to navigate the Artifactory GUI and the features available.
- Discuss the advantages and limitation of using the a bootstrap configuration file to setup Artifactory.

## Integration

1. Reconfigure your Jenkins PetClinic job to deploy artifacts to a Maven repository in Artifactory.
2. Create a Jenkins job to deploy an artifact from Artifactory to Tomcat.

# Deliverable

- Discuss the differences between Nexus and Artifactory.
- Discuss the importance and limitations of the open source version of Artifactory versus the enterprise solutions.

## Artifactory API

- Experiment with making calls to [Artifactory's REST API](https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API).
- Try to replicate some of the steps you took above with the Artifactory API instead of the GUI.

# Deliverable

- Discuss some use cases for Artifactory's REST API.
