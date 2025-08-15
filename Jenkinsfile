pipeline {
    agent {
        docker {
            image 'docker/compose:latest'
            // THIS IS THE NEW LINE TO ADD
            tool 'docker-latest'
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