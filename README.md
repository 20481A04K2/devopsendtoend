markdown
# 🚀 DevOps End-to-End CI/CD Pipeline

### Production-Grade CI/CD for a 3-Tier Application on Google Cloud Run

An end-to-end, security-hardened DevOps pipeline that takes a Python-based 3-tier user management application from source code to production deployment on **Google Cloud Run** — with automated code quality checks, multi-layer vulnerability scanning, and a manual approval gate, all orchestrated through Jenkins.

---

## 🎯 Highlights

- ✅ **Fully automated CI/CD pipeline** — 9-stage Jenkins pipeline from checkout to deployment
- ✅ **Shift-left security** — vulnerabilities caught at filesystem, image, and dependency level before deployment
- ✅ **Zero-touch deployment** — automated builds pushed to Artifact Registry and deployed to Cloud Run
- ✅ **Governed releases** — manual approval gate ensures controlled production deployments
- ✅ **Cloud-native architecture** — serverless container hosting with managed database connectivity

---

## 🏗️ Architecture

| Component | Technology |
|---|---|
| Application | Python-based 3-tier user management app |
| Containerization | Docker |
| CI/CD Orchestration | Jenkins |
| Deployment Target | Google Cloud Run (serverless, auto-scaling) |
| Image Registry | Google Artifact Registry |
| Database | Cloud SQL (MySQL) via Cloud SQL Auth Proxy |
| Code Quality | SonarQube |
| Security Scanning | Trivy, Snyk |

---

## ⚙️ Pipeline Stages

| Stage | Purpose |
|---|---|
| 1️⃣ Checkout | Pulls latest source code from GitHub |
| 2️⃣ SonarQube Analysis | Static code quality and code-smell detection |
| 3️⃣ Filesystem Security Scan (Trivy) | Scans project files for known CVEs |
| 4️⃣ Docker Image Build | Builds the containerized application image |
| 5️⃣ Image Security Scan (Trivy) | Scans the built image for vulnerabilities |
| 6️⃣ Dependency Scan (Snyk) | Identifies and flags vulnerable dependencies |
| 7️⃣ Push to Artifact Registry | Publishes the validated image to GCP |
| 8️⃣ Manual Approval Gate | Requires sign-off before production release |
| 9️⃣ Deploy to Cloud Run | Ships the approved build to production |

---

## 🛠️ Tech Stack

**Cloud & Infrastructure:** Google Cloud Run, Artifact Registry, Cloud SQL, Cloud SQL Auth Proxy
**CI/CD:** Jenkins (declarative pipeline)
**Containerization:** Docker
**Code Quality & Security:** SonarQube, Trivy, Snyk
**Languages:** Python, HTML

---

## 📁 Repository Structure

├── 3-tier-user-management-app-main/ # Application source code
├── template/ # HTML templates
├── Dockerfile # Container build definition
├── Jenkinsfile # 9-stage CI/CD pipeline definition
├── app.py # Application entry point
├── requirements.txt # Python dependencies
└── sonar-project.properties # SonarQube configuration


---

## 🚀 Getting Started

### Prerequisites
- Docker installed
- Jenkins with SonarQube Scanner, Snyk, and Pipeline Input Step plugins
- GCP project with Cloud Run, Artifact Registry, and Cloud SQL enabled
- Trivy and Snyk CLI available on the Jenkins agent

### Run Locally
```bash
docker build -t user-management-app .
docker run -p 8080:8080 user-management-app
```

### Deploy via Pipeline
Push to the `main` branch to trigger the Jenkins pipeline — it will automatically test, scan, build, and (after approval) deploy to Cloud Run.

---

## 🔐 Security-First Design

This pipeline follows a **defense-in-depth** approach to security:

- **Static analysis** with SonarQube catches code quality issues early
- **Filesystem scanning** with Trivy flags vulnerable files before build
- **Image scanning** with Trivy validates the final container before push
- **Dependency scanning** with Snyk ensures third-party packages are safe
- **Manual approval gate** prevents unreviewed changes from reaching production

---

## 📈 Outcome

Delivered a repeatable, secure, and fully automated deployment pipeline — reducing manual deployment effort and catching vulnerabilities at multiple stages before they reach production.

---

## 👤 Author

**Sajja Vamsi**
DevOps Engineer | GCP Dual-Certified
[[LinkedIn](https://linkedin.com/in/sajja-vamsi)](https://www.linkedin.com/in/sajja-vamsi-b68481250/)
