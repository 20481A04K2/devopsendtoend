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

        stage('Push to Artifact Registry') {
      steps {
        sh '''
          gcloud config set project $PROJECT_ID
          gcloud auth configure-docker $REGION-docker.pkg.dev --quiet
          docker push $AR_URL
        '''
      }
    }
    
    stage('Stage - 8 - Create MySQL Table') {
      steps {
        withCredentials([file(credentialsId: 'gcp-service-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          sh '''
            sudo apt-get update && sudo apt-get install -y mysql-client

            wget -q https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
            chmod +x cloud_sql_proxy

            trap 'pkill -f cloud_sql_proxy' EXIT
            ./cloud_sql_proxy -dir=/cloudsql -instances=${INSTANCE_CONNECTION_NAME} &
            sleep 10

            echo "Creating table if not exists..."
            mysql --host=127.0.0.1 --user=${DB_USER} --password=${DB_PASSWORD} --database=${DB_NAME} -e "
              CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                city VARCHAR(100)
              );
            "
          '''
        }
      }
    }

    stage('Stage - 9 - Deploy to Cloud Run') {
      steps {
        withCredentials([file(credentialsId: 'gcp-service-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          sh '''
            gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
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
