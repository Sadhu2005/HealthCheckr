pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building the Docker images...'
                sh 'docker-compose build'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                sh 'docker-compose down' // Stop any old running containers
                sh 'docker-compose up -d' // Start new containers in detached mode
            }
        }
    }
}