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

## Initialize

### Set the PROJECT_ID environment variable

Set the PROJECT_ID environment variable. This variable will be used in forthcoming steps.
```bash
export PROJECT_ID=<walkthrough-project-id/>
```

### Enable needed APIs and Create Google Cloud Deploy pipeline
The `init.sh` script in the `bootstrap` folder enables your APIs, customizes your clouddeploy.yaml and creates a Cloud Deploy pipeline for you. You'll still need to do some steps manually after these scripts run, though.

1. Run the init script
```bash
. ./bootstrap/init.sh
```

### Check out your Google Cloud Deploy Pipeline

Verify that the Google Cloud Deploy pipeline was created in [Google Cloud Deploy UI](https:///console.cloud.google.com/deploy/delivery-pipelines)

## Setup a Cloud Build trigger for your repo
  * Navigate to [Cloud Build triggers page](https://console.cloud.google.com/cloud-build/triggers)
  * Follow the [docs](https://cloud.google.com/build/docs/automating-builds/build-repos-from-github) and create a Github App connected repo and trigger.

## Create GKE clusters
You'll need GKE clusters to deploy to. The Google Cloud Deploy pipeline in this example refers to three clusters:
* testcluster
* stagingcluster
* productcluster

If you have/want different cluster names update cluster definitions in:
* <walkthrough-editor-select-regex filePath="bootstrap/gke-cluster-init.sh" regex="cluster">bootstrap / gke-cluster-init.sh</walkthrough-editor-select-regex>
* <walkthrough-editor-select-regex filePath="clouddeploy.yaml" regex="cluster">clouddeploy.yaml</walkthrough-editor-select-regex>


### Create the three GKE Autopilot clusters

```bash
. ./bootstrap/gke-cluster-init.sh
```

## IAM and service account setup
You must give Cloud Build explicit permission to trigger a Google Cloud Deploy release.
1. Read the [docs](https://cloud.google.com/deploy/docs/integrating)
2. Navigate to IAM and locate your Cloud Build service account
3. Add these two roles
  * Cloud Deploy Releaser
  * Service Account User

## Demo
The demo flow outlines a typical developer pathway, submitting a change to a Git repo which then triggers a CI/CD process:
1. User commits a change the main branch of the repo
2. Cloud Build is automatically triggered, which:
  * builds and pushes impages to Artifact Registry
  * creates a Google Cloud Deploy release in the pipeline
3. User then navigates to Google Cloud Deploy UI and shows promotion events:
  * test cluster to staging clusters
  * staging cluster to product cluster, with approval gate

## Tear down

To remove the three running GKE clusters, run:
```bash
. ./bootstrap/gke-cluster-delete.sh
```

## Local dev

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