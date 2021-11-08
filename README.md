# Purpose
This repo demostrates Kubernetes development and deployment with Skaffold and Kustomize. It is based on a simple Python Flask example app named "Population Stats". 

# Try it in Cloud Shell
Google Cloud Shell provides a free environment in which to play with these files:

[![Open in cloud shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/vszal/pop-kustomize&page=editor&open_in_editor=skaffold.yaml)

# K8s / Kustomize configuration

TODO - directory structure, clarify this section

`k8s/base` - base config files
`k8s/overlays` - overlays including dev, staging and prod. "dev" overlay maps to default Skaffold deploy.

# Building, Deploying & Running
While there are several ways to build and run the app in this repo, the intention is to demonstrate Skaffold and Kustomize in local development scenarios ("dev"), as well as deployments to two additional environments: "staging" and "prod". 

## Local dev
To run this app locally, start minikube or some other local k8s framework and from the root of the repo run:

`skaffold dev`

This profile uses the "dev" customer overlay.

Once running, you can make file changes and observe the rebuilding of the container and redeployment.

## Staging 
To deploy to staging, set your kube context to the proper cluster and run:

`skaffold run --profile staging`

## Prod
To deploy to prod, set your kube context to the proper cluster and run:

`skaffold run --profile prod`

# Population stats

Simple web app that pulls population data based on address queries. 

Population data gathered from the U.S. Census Bureau [Population Estimate API](https://www.census.gov/data/developers/data-sets/popest-popproj/popest.html).

# Build with Google Cloud Build
Serverless CI / build:

`gcloud builds submit app --config=cloudbuild.yaml`