pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building the Docker images...'
                // Changed from docker-compose to docker compose
                sh 'docker compose build'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                // Changed from docker-compose to docker compose
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }
    }
}