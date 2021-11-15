# Google Cloud CI/CD End-to-End Demo
This repo demostrates Kubernetes development and deployment with Skaffold and Google Cloud devops tools Google Cloud Deploy, Cloud Build, and Artifact Registry. The example app is based on a simple Python Flask example app named "Population Stats" and uses Kustomize overlays for manifest generation. 

## Create a repo
This demo relies on you making git check-ins to simulate a developer workflow. Fork this repo, or otherwise copy it into your own Github repo.

## Customize Cloud Deploy yaml

1. In `clouddeploy.yaml`, replace `project-id-here` with your actual project for each of the three targets.

## Bootstrap Google Cloud demo
Bootstrap scripts are in the `bootstrap` folder.

The `init.sh` script is provided to bootstrap much of the configuration setup. You'll still need to do some steps manually after this script runs though.

1. In `init.sh`, replace project-id-here with your Google Cloud project-id on line 3.
2. Run `. ./bootstrap/init.sh`
3. Verify that the Google Cloud Deploy pipeline was created in [Google Cloud Deploy UI](https://console.google.com/deploy/delivery-pipelines)
4. Setup a Cloud Build trigger for your repo
  * Navigate to [Cloud Build triggers page](https://console.google.com/cloud-build/triggers)
  * Follow the [docs](https://cloud.google.com/build/docs/automating-builds/build-repos-from-github) and create a Github App connected repo and trigger.

## Create GKE clusters
You'll need GKE clusters to deploy out to as part of the demo. This repo refers to three clusters:
* testcluster
* stagingcluster
* productcluster

If you have/want different cluster names update cluster definitions in the gke-cluster-init.sh bash script and in clouddeploy.yaml

To create the clusters, edit `bootstrap/gke-cluster-init.sh`:
1. Replace `project-id-here` with your project-id on line 3.
2. Run `. ./bootstrap/gke-cluster-init.sh`

## IAM and service account setup
You must give Cloud Build explicit permission to trigger a Cloud Deploy release.
1. Read the [docs](https://cloud.google.com/deploy/docs/integrating)
2. Navigate to IAM and locate your Cloud Build service account
3. Add these two roles
  * Cloud Deploy Releaser
  * Service Account User

## Demo
The demo is very simple at this stage.
1. User commits a change the main branch of the repo
2. Cloud Build is automatically triggered, which:
  * builds and pushes impages to Artifact Registry
  * creates a Cloud Deploy release in the pipeline
3. User then navigates to Cloud Deploy UI and shows promotion events:
  * test cluster to staging clusters
  * staging cluster to product cluster, with approval gate

## Tear down
To remove the three running GKE clusters, edit `bootstrap/gke-cluster-delete.sh`:
1. Replace `project-id-here` with your project-id on line 3.
2. Run `. ./bootstrap/gke-cluster-delete.sh`

# Local dev
To run this app locally, start minikube or some other local k8s framework and from the root of the repo run:

`skaffold dev`

The default skaffold settings use the "dev" customer overlay. 

Once running, you can make file changes and observe the rebuilding of the container and redeployment.

To test the staging overlays/profile:

`skaffold run --profile staging`

To test the staging overlays/profile:

`skaffold run --profile prod`

## Try it in Cloud Shell
Google Cloud Shell provides a free environment in which to play with these files:

[![Open in cloud shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/vszal/pop-kustomize&page=editor&open_in_editor=skaffold.yaml)

# About the Sample app - Population stats

Simple web app that pulls population data based on address queries. 

Population data gathered from the U.S. Census Bureau [Population Estimate API](https://www.census.gov/data/developers/data-sets/popest-popproj/popest.html).
