# Description: Check if minikube is not running, then start minikube

#!/bin/bash
STATUS=$(minikube status --format='{{.Host}}')

if [ "$STATUS" != "Running" ]; then
    minikube start --driver=docker
fi
