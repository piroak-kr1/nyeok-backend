# Description: Start local database for development

# Start minikube if not running
scripts_dir=$(dirname "$0")
start_minikube="$scripts_dir/start_minikube.sh"
"$start_minikube"

kubectl port-forward svc/postgres-svc 5432:5432
