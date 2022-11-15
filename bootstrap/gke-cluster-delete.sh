# Cleanup script to delete the three clusters created by the gke-cluster-init.sh script
# bail if PROJECT_ID is not set
if [[ -z "${PROJECT_ID}" ]]; then
  echo "The value of PROJECT_ID is not set. Be sure to run export PROJECT_ID=YOUR-PROJECT first"
  return
fi
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