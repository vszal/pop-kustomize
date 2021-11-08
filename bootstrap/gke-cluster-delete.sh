# Cleanup script to delete the three clusters created by the gke-cluster-init.sh script
# ACTION REQUIRED! Change "project-id-here" value to the project you'll be using
export PROJECT_ID="project-id-here"
# sets the current project for gcloud
gcloud config set project $PROJECT_ID
# Test cluster
echo "Deleting testcluster..."
gcloud container clusters delete testcluster --region "us-central1" --async
# Staging cluster
echo "Deleting stagingcluster..."
gcloud container clusters delete stagingcluster --region "us-central1" --async
# Prod cluster
echo "Deleting prodcluster..."
gcloud container clusters delete prodcluster --region "us-central1" --async