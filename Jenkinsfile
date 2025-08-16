pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building the Docker images...'
                // Use the classic docker-compose (with a hyphen) command
                sh 'docker-compose build'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                sh 'docker-compose down'
                sh 'docker-compose up -d'
            }
        }
    }
}