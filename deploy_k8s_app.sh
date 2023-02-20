#!/bin/bash

# Deleta todos pods, services, e deployments existentes
kubectl delete deployment mysql-deployment
kubectl delete service mysql-service
kubectl delete deployment db-service-deployment
kubectl delete service db-service
kubectl delete deployment web-service-deployment
kubectl delete service web-service
kubectl delete deployment ml-service-deployment
kubectl delete service ml-service
kubectl delete configmap init-sql
kubectl delete persistentvolumeclaims mysql-pv
kubectl delete persistentvolume mysql-pv

# Build todas as images Docker
docker build -t db-service db-service/
docker build -t web-service web-service/
docker build -t ml-service ml-service/

# Aplica todos manifestos Kubernetes
kubectl apply -f mysql-db/mysql-persistentvolumeclaim.yml
kubectl apply -f mysql-db/mysql-persistentvolume.yml
kubectl apply -f mysql-db/init-sql-configmap.yml
kubectl apply -f mysql-db/mysql-deployment.yml
kubectl apply -f mysql-db/mysql-service.yml
kubectl apply -f db-service/db-deployment.yml
kubectl apply -f db-service/db-service.yml
kubectl apply -f ml-service/ml-deployment.yml
kubectl apply -f ml-service/ml-service.yml
kubectl apply -f web-service/web-deployment.yml
kubectl apply -f web-service/web-service.yml
