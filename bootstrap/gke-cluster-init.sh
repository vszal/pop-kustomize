# Creates 3 GKE autopilot clusters
# Initializes APIS, sets up the Google Cloud Deploy pipeline
# bail if PROJECT_ID is not set
if [[ -z "${PROJECT_ID}" ]]; then
  echo "The value of PROJECT_ID is not set. Be sure to run export PROJECT_ID=YOUR-PROJECT first"
  return
fi
# Test cluster
echo "creating testcluster..."
gcloud beta container --project "$PROJECT_ID" clusters create-auto "testcluster" \
--region "us-central1" --release-channel "regular" --network "projects/$PROJECT_ID/global/networks/default" \
--subnetwork "projects/$PROJECT_ID/regions/us-central1/subnetworks/default" \
--cluster-ipv4-cidr "/17" --services-ipv4-cidr "/22" --async
# Staging cluster
echo "creating stagingcluster..."
gcloud beta container --project "$PROJECT_ID" clusters create-auto "stagingcluster" \
--region "us-central1" --release-channel "regular" --network "projects/$PROJECT_ID/global/networks/default" \
--subnetwork "projects/$PROJECT_ID/regions/us-central1/subnetworks/default" \
--cluster-ipv4-cidr "/17" --services-ipv4-cidr "/22" --async
# Prod cluster
echo "creating prodcluster..."
gcloud beta container --project "$PROJECT_ID" clusters create-auto "prodcluster" \
--region "us-central1" --release-channel "regular" --network "projects/$PROJECT_ID/global/networks/default" \
--subnetwork "projects/$PROJECT_ID/regions/us-central1/subnetworks/default" \
--cluster-ipv4-cidr "/17" --services-ipv4-cidr "/22" --async
echo "Creating clusters! Check the UI for progress"