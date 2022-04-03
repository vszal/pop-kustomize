<walkthrough-metadata>
  <meta name="title" content="Google Cloud CI/CD End-to-End Demo" />
  <meta name="description" content="Guide for helping you get up and running with Google Cloud CI/CD" />
  <meta name="component_id" content="102" />
</walkthrough-metadata>

<walkthrough-disable-features toc></walkthrough-disable-features>

# Google Cloud End to End CI/CD tutorial
This tutorial will help you get up and running with Google Cloud CI/CD, including Cloud Build, Google Cloud Deploy, and Artifact Registry

## Select a project

<walkthrough-project-setup billing="true"></walkthrough-project-setup>

Once you've selected a project, click "Start".

## Set the PROJECT_ID environment variable

Set the PROJECT_ID environment variable. This variable will be used in forthcoming steps.
```bash
export PROJECT_ID=<walkthrough-project-id/>
```

### Enable needed APIs and Create Google Cloud Deploy pipeline
The 
<walkthrough-editor-open-file filePath="bootstrap/init.sh">bootstrap/init.sh</walkthrough-editor-open-file>
script enables your APIs, customizes your 
<walkthrough-editor-open-file filePath="clouddeploy.yaml">
clouddeploy.yaml
</walkthrough-editor-open-file> 
and creates a Cloud Deploy pipeline for you. You'll still need to do some steps manually after these scripts run, though.

Run the initialization script:
```bash
. ./bootstrap/init.sh
```

### Check out your Google Cloud Deploy Pipeline

Verify that the Google Cloud Deploy pipeline was created in the 
[Google Cloud Deploy UI](https://console.cloud.google.com/deploy/delivery-pipelines)

## (Optional) Turn on automated container vulnerability analysis
Google Cloud Container Analysis can be set to automatically scan for vulnerabilities on push (see [pricing](https://cloud.google.com/container-analysis/pricing)). 

To enable automated scanning, enable the Container Analysis API:

```bash
gcloud services enable containerscanning.googleapis.com
```

## Configure your Github.com repo

If you have not fork this repo yet, please do so now:

[Fork this repo on Github](https://github.com/vszal/pop-kustomize/fork)

To keep file changes you make in Cloud Shell in sync with your repo, you can check these file changes into your new Github repo by following these [docs](https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github). Note that the Github CLI is available in Cloud Shell.


## Setup a Cloud Build trigger for your repo
Now that your Github repo is setup, configure Cloud Build to run each time a change is pushed to the main branch. To do this, add a Trigger in Cloud Build:
  * Navigate to [Cloud Build triggers page](https://console.cloud.google.com/cloud-build/triggers)
  * Follow the [docs](https://cloud.google.com/build/docs/automating-builds/build-repos-from-github) and create a Github App connected repo and trigger.

## Create GKE clusters
You'll need GKE clusters to deploy to. The Google Cloud Deploy pipeline in this example refers to three clusters:
* testcluster
* stagingcluster
* productcluster

If you have/want different cluster names update cluster definitions in:
* <walkthrough-editor-select-regex filePath="bootstrap/gke-cluster-init.sh" regex="cluster">bootstrap/gke-cluster-init.sh</walkthrough-editor-select-regex>
* <walkthrough-editor-select-regex filePath="clouddeploy.yaml" regex="cluster">clouddeploy.yaml</walkthrough-editor-select-regex>
* <walkthrough-editor-select-regex filePath="bootstrap/gke-cluster-delete.sh" regex="cluster">bootstrap/gke-cluster-delete.sh</walkthrough-editor-select-regex>


### Create the three GKE Autopilot clusters

```bash
. ./bootstrap/gke-cluster-init.sh
```

## IAM and service account setup
You must give Cloud Build explicit permission to trigger a Google Cloud Deploy release.
1. Read the [docs](https://cloud.google.com/deploy/docs/integrating)
2. Navigate to [IAM](https://console.cloud.google.com/iam-admin/iam) and locate your Cloud Build service account
3. Add these two roles
  * Cloud Deploy Releaser
  * Service Account User


## Demo Overview

[![Demo flow](https://user-images.githubusercontent.com/76225123/145627874-86971a34-768b-4fc0-9e96-d7a769961321.png)](https://user-images.githubusercontent.com/76225123/145627874-86971a34-768b-4fc0-9e96-d7a769961321.png)

The demo flow outlines a typical developer pathway, submitting a change to a Git repo which then triggers a CI/CD process:
1. Push a change the main branch of your forked repo. You can make any change such as a trivial change to the README.md file.
2. A Cloud Build job is automatically triggered, using the <walkthrough-editor-open-file filePath="cloudbuild.yaml">
cloudbuild.yaml</walkthrough-editor-open-file>  configuration file, which:
  * builds and pushes impages to Artifact Registry
  * creates a Google Cloud Deploy release in the pipeline
3. You can then navigate to Google Cloud Deploy UI and shows promotion events:
  * test cluster to staging clusters
  * staging cluster to product cluster, with approval gate


## Tear down

To remove the three running GKE clusters, run:
```bash
. ./bootstrap/gke-cluster-delete.sh
```

## Local dev (optional)

To run this app locally, start minikube:
```bash 
minikube start
```

From the pop-kustomize directory, run:
```bash
skaffold dev
```

The default skaffold settings use the "dev" Kustomize overlay. Once running, you can make file changes and observe the rebuilding of the container and redeployment. Use Ctrl-C to stop the Skaffold process.

To test the staging overlays/profile run:
```bash
skaffold dev --profile staging
```

To test the staging overlays/profile locally, run:
```bash
skaffold dev --profile prod
```