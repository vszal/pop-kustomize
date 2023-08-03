# Demo: Devops Best Practices

This repo is a fork of https://github.com/nateaveryg/pop-kustomize which is meant to demonstrate
setting up a project in GCP that follows devops best practices.

The demo will be used to display:
- [x] Cloud workstations
- [] GCB triggering
- [] Build and push to AR
- [] Image scanning (AR can do this on push)
- [] Provenance generation
- [] Cloud Deploy promotion across environments
- [] Cloud Deploy canary deployment
- [] Cloud Deploy label: allows link back to git sha
- [] DORA stats (Cloud Deploy?)
- [] Security insights in Cloud Deploy (can show cloud build panel at least, ideally both)
- [] Binauthz gating of deployment

## Setup tutorial

After forking the repo, follow along here.

## Setup: enable APIs

Set the PROJECT_ID environment variable. This variable will be used in forthcoming steps.

```bash
export PROJECT_ID=<walkthrough-project-id/>
# sets the current project for gcloud
gcloud config set project $PROJECT_ID
# Enables various APIs you'll need
gcloud services enable container.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com clouddeploy.googleapis.com \
  cloudresourcemanager.googleapis.com \ secretmanager.googleapis.com
```

## Setup a Cloud Build trigger for your repo

Configure Cloud Build to run each time a change is pushed to the main branch. To do this, add a Trigger in Cloud Build:
  1. Follow https://cloud.google.com/build/docs/automating-builds/github/connect-repo-github to connect
     your GitHub repo
  2. Follow https://cloud.google.com/build/docs/automating-builds/github/build-repos-from-github?generation=2nd-gen to setup triggering:
    * Setup PR triggering to run cloudbuild-test.yaml
    * Setup triggering on the `main` branch to run cloudbuild-deploy.yaml

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

Enable Container Analysis API for automated scanning:

<walkthrough-enable-apis apis="containerscanning.googleapis.com"></walkthrough-enable-apis>


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

Note that these clusters are created asynchronously, so check on the [GKE UI]("https://console.cloud.google.com/kubernetes/list/overview") periodically to ensure that the clusters are up before submitting your first release to Google Cloud Deploy.

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
## About the Sample app - Population stats

Simple web app that pulls population and flag data based on country query.

Population data from restcountries.com API.

Feedback and contributions welcomed!
