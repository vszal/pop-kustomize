# Demo: Google Cloud CI/CD for GKE
This repo demostrates CI/CD for GKE with Google Cloud tools Google Cloud Deploy, Cloud Build, and Artifact Registry. The example app is based on a simple Python Flask example app named "Population Stats" and uses Kustomize overlays to enable configuration differences across three different environments: test, staging, and prod. 

[![Demo flow](https://user-images.githubusercontent.com/76225123/145627874-86971a34-768b-4fc0-9e96-d7a769961321.png)](https://user-images.githubusercontent.com/76225123/145627874-86971a34-768b-4fc0-9e96-d7a769961321.png)

## Fork this repo
This demo relies on you making git check-ins to simulate a developer workflow. So you'll need your own copy of these files in your own Github.com repo.

[Fork this repo on Github](https://github.com/vszal/pop-kustomize/fork)

If you've already done that, you can start the setup tutorial below.

## Setup tutorial
The following tutorial walks you through all the setup needed to configure Google Cloud services needed to run this demo. Clicking this button provisions a Cloud Shell Editor and launches an interactive tutorial which steps you through the process. Google Cloud account and project required.

[![Start tutorial in cloud shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/open?git_repo=https://github.com/vszal/pop-kustomize&cloudshell_workspace=.&cloudshell_tutorial=tutorial.md)

If you don't want to run the tutorial in Cloud Shell, you can view the md file [here](https://github.com/vszal/pop-kustomize/blob/main/tutorial.md).

## About the Sample app - Population stats

Simple web app that pulls population data based on U.S. address queries. Note, other countries are currently not supported.

Population data gathered from the U.S. Census Bureau [Population Estimate API](https://www.census.gov/data/developers/data-sets/popest-popproj/popest.html). 

Feedback and contributions welcomed!
