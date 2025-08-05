pipeline {
  agent any

  environment {
    PROJECT_ID = 'sylvan-hydra-464904-d9'
    REGION = 'us-central1'
    REPO = 'devops-app'
    IMAGE_NAME = 'user-management-app'
    FULL_IMAGE_NAME = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}"
    INSTANCE_CONNECTION_NAME = 'sylvan-hydra-464904-d9:us-central1:my-app-db'
    DB_USER = 'appuser'
    DB_PASSWORD = 'Praveen@123'
    DB_NAME = 'user_management'
    SERVICE_NAME = 'myapp'
  }

  stages {

    stage('Stage - 1 - Checkout') {
      steps {
        git branch: 'main',
            url: 'https://github.com/20481A04K2/devopsendtoend.git'
      }
    }

    stage('Stage - 2 - SonarQube Analysis') {
      steps {
        withSonarQubeEnv('MySonar') {
          sh '''
            echo "🔍 Running SonarQube Scanner..."
            /opt/sonar-scanner/bin/sonar-scanner \
              -Dsonar.projectKey=my-python-app \
              -Dsonar.sources=. \
              -Dsonar.host.url=http://35.184.37.88:9000 \
              -Dsonar.login=sqa_181f243156df8fba2682acfca191637ce7f5af32
          '''
        }
      }
    }

    stage('Stage - 3 - Filesystem Security Scan - Trivy') {
      steps {
        sh '''
          trivy fs . --exit-code 0 --severity MEDIUM,HIGH,CRITICAL
        '''
      }
    }

    stage('Stage - 4 - Docker Image Build') {
      steps {
        sh '''
          echo "🐳 Building Docker image..."
          docker build -t ${FULL_IMAGE_NAME}:latest .
        '''
      }
    }

    stage('Stage - 5 - Docker Image Security Scan - Trivy') {
      steps {
        sh '''
          mkdir -p $WORKSPACE/trivy-cache
          trivy image \
            --exit-code 0 \
            --severity MEDIUM,HIGH,CRITICAL \
            --cache-dir $WORKSPACE/trivy-cache \
            ${FULL_IMAGE_NAME}:latest
        '''
      }
    }

    stage('Stage - 6 - Fix Vulnerability by Snyk') {
      steps {
        withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
          sh '''
            npm install snyk
            npx snyk auth $SNYK_TOKEN
            npx snyk test
          '''
        }
      }
    }

    stage('Stage - 7 - Push to Artifact Registry') {
      steps {
        sh '''
          echo "📦 Pushing Docker image to Artifact Registry..."
          gcloud config set project ${PROJECT_ID}
          gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
          docker push ${FULL_IMAGE_NAME}:latest
        '''
      }
    }

    stage('Stage - 8 - Approval for Deployment') {
      steps {
        script {
          input message: "🛑 Do you approve deployment to Cloud Run?", ok: "✅ Deploy", submitter: "sajja_vamsi"
        }
      }
    }

    stage('Stage - 9 - Deploy to Cloud Run') {
      steps {
        sh '''
          echo "🚀 Deploying to Cloud Run..."
          gcloud config set project ${PROJECT_ID}
          gcloud run deploy ${SERVICE_NAME} \
            --image ${FULL_IMAGE_NAME}:latest \
            --platform managed \
            --region ${REGION} \
            --allow-unauthenticated \
            --set-env-vars INSTANCE_CONNECTION_NAME=${INSTANCE_CONNECTION_NAME},DB_USER=${DB_USER},DB_PASSWORD=${DB_PASSWORD},DB_NAME=${DB_NAME}
        '''
      }
    }
  }

  post {
    always {
      echo "📝 Pipeline execution completed."
    }
    success {
      echo "✅ Deployment was successful!"
    }
    failure {
      echo "❌ Something went wrong."
    }
  }
}
