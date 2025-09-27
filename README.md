# 🏆 Guestbook App Challenge - Python, Flask, MySQL, Docker & Kubernetes

A fast web-based guestbook application built with Flask and MySQL, containerized with Docker, and deployed on Kubernetes using Helm as part of a challenge for S*****l.

## ✨ Resume

- ✅ Responsive web interface built with Flask
- ✅ MySQL database with persistence
- ✅ Containerized with Docker
- ✅ Deployed on Kubernetes using Helm
- ✅ Nginx Ingress for routing
- ✅ GitOps-ready configuration

## 🏗️ Flowchart

![Flowchart](docs/images/Flowchart.png)

# 🚀 Fast Deployment

# Using Docker Compose (Development)

```shell
git clone https://github.com/chispa77/guestbook-app.git
cd guestbook-app/docker
cp .env.example .env
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

2. **Deploy app in K8s-interview-01 Cluster**

```shell
# Install Helm chart
git clone https://github.com/chispa77/guestbook-app.git
cd guestbook-app/k8s-helm
helm install guestbook-release -n guestbook-app --create-namespace
```

3. **Access the Application**

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

# 📚 Project Structure

* ```docker/``` - Dockerfile and Docker Compose configuration

* ```docker/src/``` - Source Code of the Flask Application

* ```k8s-helm/``` - Helm chart for Kubernetes

* ```docs/``` - Images

* ```scripts/``` - Testing scripts

# 🔧 Tech Stack

* **Backend:** Python, Flask

* **Database:** MySQL 8.0

* **Containerization:** Docker

* **Orchestration:** Kubernetes

* **Package Management:** Helm

* **Reverse Proxy:** Nginx Ingress

👨‍💻 Autor
[Christian Roldan] - [christian_roldan@hotmail.com]