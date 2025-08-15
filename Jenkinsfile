pipeline {
    agent any

    tools {
        // This line finds the 'docker-latest' tool you configured
        // in the UI and adds its commands to the system PATH.
        tool 'docker-latest'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the Docker images...'
                // This command will now work because the 'tools' block made it available.
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