pipeline {
    agent any

    tools {
        // This is the corrected line.
        // It uses the correct type 'dockerTool' and the name 'docker-latest'
        // that you configured in the Jenkins UI.
        dockerTool 'docker-latest'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the Docker images...'
                sh 'docker compose build'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }
    }
}