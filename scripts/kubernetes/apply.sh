# Description: Run apply -k for minikube or gke

# Always update secret file
cp ./backend-service/backend_service/.secret ./k8s/base/.secret.backend

if [[ "$1" == "minikube" ]]; then
  # Start minikube if not running
  scripts_dir=$(dirname "$0")
  start_minikube="$scripts_dir/start_minikube.sh"
  "$start_minikube"
  
  kubectl config use-context "$1"
  kubectl apply -k ./k8s/overlays/"$1"
  
  echo ""
  echo "Minikube available at: http://localhost, http://localhost/api"
  
  minikube tunnel
elif [[ "$1" == "gke" ]]; then
  kubectl config use-context "$1"
  kubectl apply -k ./k8s/overlays/"$1"
  
  echo ""
  echo "GKE availabe at: https://piroak.com"
else
  echo "Usage: ./kapply.sh minikube|gke"
fi
