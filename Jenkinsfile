pipeline {
    // This block tells Jenkins to run the pipeline inside a container
    // that has Docker and Docker Compose tools pre-installed.
    agent {
        docker {
            image 'docker/compose:latest'
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
        }
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