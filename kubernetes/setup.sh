#!/bin/bash

set -e

echo "🚀 Initializing VoiceSync Kubernetes Cluster..."

# Create namespace
echo "📦 Creating namespace..."
kubectl create namespace voicesync || true

# Label namespace for network policies
kubectl label namespace voicesync name=voicesync --overwrite

# Create storage class
echo "💾 Creating storage class..."
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/host-path
parameters:
  type: pd-ssd
EOF

# Apply deployments
echo "🎯 Applying deployments..."
kubectl apply -f kubernetes/deployment.yaml

# Apply load balancer
echo "⚖️ Applying load balancer..."
kubectl apply -f kubernetes/load-balancer.yaml

# Apply ingress
echo "🌐 Applying ingress..."
kubectl apply -f kubernetes/ingress.yaml

# Apply monitoring
echo "📊 Applying monitoring..."
kubectl apply -f kubernetes/monitoring.yaml

# Wait for deployments
echo "⏳ Waiting for deployments to be ready..."
kubectl rollout status deployment/api -n voicesync --timeout=5m
kubectl rollout status deployment/analytics -n voicesync --timeout=5m
kubectl rollout status deployment/nginx-lb -n voicesync --timeout=5m

echo "✅ Kubernetes cluster initialized successfully!"
echo ""
echo "📋 Useful commands:"
echo "  kubectl get pods -n voicesync"
echo "  kubectl get services -n voicesync"
echo "  kubectl logs -f deployment/api -n voicesync"
echo "  kubectl port-forward svc/api-service 8000:8000 -n voicesync"
echo "  kubectl port-forward svc/prometheus 9090:9090 -n voicesync"
