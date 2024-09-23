#!/bin/bash
STATUS=$(minikube status --format='{{.Host}}')

if [ "$STATUS" != "Running" ]; then
    minikube start --driver=docker
    # NOTE: minikube start is not long-running process. It finishes
fi
