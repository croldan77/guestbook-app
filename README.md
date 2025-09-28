# 🏆 Guestbook App Challenge - Python, Flask, MySQL, Docker & Kubernetes

A fast web-based guestbook application built with Flask and MySQL, containerized with Docker, and deployed on Kubernetes using Helm as part of a challenge for S*****l.

## ✨ Resume

- ✅ Responsive web interface built with Flask
- ✅ MySQL database with persistence
- ✅ Containerized with Docker
- ✅ Deployed on Kubernetes using Helm
- ✅ Nginx Ingress for routing
- ✅ GitOps-ready configuration (In Progress)

## Architecture

![Architecture](docs/images/Architecture.png)

## 🏗️ Flowchart

![Flowchart](docs/images/Flowchart.png)

# 🚀 Fast Deployment

# Using Docker Compose (Development)

```shell
git clone https://github.com/chispa77/guestbook-app.git
cd guestbook-app/docker
cp .env.example .env
# Desplegar con variables de entorno
export MYSQL_PASSWORD=[guestbook_user_password]
export MYSQL_ROOT_PASSWORD=[root_password]
docker-compose up -d
```
## 🐳 Docker Image Management

### Build and Publish the Image

1. **Build the image locally:**

```shell
docker build -t guestbook-app:v1.3.0 .
```

2. **Tagging for Docker Hub:**

```shell
docker tag guestbook-app:v1.3.0 chisporra77/guestbook-app:1.3.0
```

3. **Login and push to Docker Hub:**

```shell
docker login
docker push chisporra77/guestbook-app:v1.3.0
```

## Multi-architecture (Apple Silicon/AMD64)

### To support multiple architectures:

```shell
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t chisporra77/guestbook-app:latestv.1.3.0 --push .
```

# Using Kubernetes (Production)

1. **Connect to K8s-interview-01 Cluster**

```shell
brew install doctl
doctl auth init -t 
doctl kubernetes cluster kubeconfig save 9e15da88-8f51-4aca-b99a-4075e8bcd281
```

2. **Dependencies**

```shell
# Create a PGP key pair
export KEY_NAME="Your name"
export KEY_COMMENT="Key for helm-secrets"

gpg --batch --full-generate-key <<EOF
%no-protection
Key-Type: 1
Key-Length: 4096
Subkey-Type: 1
Subkey-Length: 4096
Expire-Date: 0
Name-Comment: ${KEY_COMMENT}
Name-Real: ${KEY_NAME}
EOF
```

```shell
# Obtain the fingerprint of the public key, which you will need to configure SOPS
gpg --list-secret-keys "${KEY_NAME}"
```

```yaml
# .sops.yaml
creation_rules:
  - pgp: >-
      BE574406FE117762E9F4C8B01CB98A820DCBA0FC  # Replace with your fingerprint
```

### Note: To edit secrets you can use this script

```shell
./edit-secrets.sh
```

3. **Deploy app in K8s-interview-01 Cluster**

```shell
# Install Helm chart
git clone https://github.com/chispa77/guestbook-app.git
cd guestbook-app/k8s-helm
./deploy.sh 
```

4. **Access the Application**

```shell
# Get the IP address of the Ingress
kubectl get ingress -n guestbook-app
```

```shell
# Add entry to /etc/hosts (Linux/Mac)
echo "[IP address obtained] guestbook.local" | sudo tee -a /etc/hosts
```

# 💡 How to Test Endpoints

* Get messages (GET):

```shell
curl http://guestbook.local/guestbook
```

* Send a message (POST via JSON):

```shell
curl -X POST http://guestbook.local/guestbook \
-H "Content-Type: application/json" \
-d '{"name":"Chris", "message":"Testing the API!"}'
```
# 🔧 Useful commands

### View resources

```shell
# View pods in all namespaces
kubectl get pods -A
kubectl get pods --all-namespaces

# View pods in a specific namespace
kubectl get pods -n guestbook-app

# View multiple types of resources
kubectl get pods,svc,deploy -n guestbook-app

# View everything in one namespace
kubectl get all -n guestbook-app
```

### Detailed information

```shell
# Detailed description of a pod
kubectl describe pod nombre-pod -n guestbook-app

# View logs of a pod
kubectl logs nombre-pod -n guestbook-app
kubectl logs -f nombre-pod -n guestbook-app  # follow (Real Time)

# View logs for a deployment
kubectl logs deploy/nombre-deployment -n guestbook-app
```

### Services & Networking

```shell
# View services
kubectl get services -A
kubectl get svc -n guestbook-app

# Port forwarding to access services
kubectl port-forward pod/nombre-pod -n guestbook-app 5000:80
kubectl port-forward pod/mysql-pod -n guestbook-app 3306:3306
#kubectl port-forward svc/argocd-server -n argocd 8080:443

# View endpoints
kubectl get endpoints -n argocd
```

### Configmap & Secrets

```shell
# View secrets
kubectl get secrets -n guestbook-app
kubectl describe secret nombre-secret -n guestbook-app

# View configmaps
kubectl get configmaps -n guestbook-app
kubectl describe configmap nombre-cm -n guestbook-app
```

### TROUBLESHOOTING COMMANDS

```shell
# Running commands inside a pod
kubectl exec -it nombre-pod -n guestbook-app -- /bin/bash

# View events (very useful for debugging)
kubectl get events -n guestbook-app --sort-by=.metadata.creationTimestamp
kubectl get events -A --sort-by=.metadata.creationTimestamp

# View resources with wide output
kubectl get pods -n guestbook-app -o wide
kubectl get nodes -o wide

# View cluster information
kubectl cluster-info
kubectl version
```

# 🔧 Tech Stack

* **Backend:** Python 3.9 + Flask

* **Database:** MySQL 8.0

* **Containerization:** Docker

* **Orchestration:** Kubernetes

* **Package Management:** Helm

* **Reverse Proxy:** Nginx Ingress

* **Secrets Management:** SOPS + PGP

# 📚 Project Structure

* ```docker/``` - Dockerfile and Docker Compose configuration

* ```docker/src/``` - Source Code of the Flask Application

* ```k8s-helm/``` - Helm chart for Kubernetes

* ```docs/``` - Images

* ```scripts/``` - Testing scripts


👨‍💻 Autor
[Christian Roldan] - [christian_roldan@hotmail.com]