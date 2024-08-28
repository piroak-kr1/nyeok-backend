# Description: Run apply -k for minikube or gke

if [[ "$1" == "minikube" ]]; then
  # Start minikube if not running
  scripts_dir=$(dirname "$0")
  start_minikube="$scripts_dir/start_minikube.sh"
  "$start_minikube"
fi
if [[ "$1" == "minikube" || "$1" == "gke" ]]; then
  kubectl config use-context "$1"
  # kubectl delete secret --all
  # kubectl create secret generic cluster-secret \
  #   --from-file=secret-backend=.k8s/.secret.backend \
  #   --from-file=cloudflare-token=.k8s/.secret.cloudflare
  kubectl apply -k ./k8s/overlays/"$1"
else
  echo "Usage: ./kapply.sh minikube|gke"
fi
