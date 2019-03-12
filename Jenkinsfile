pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('sonarqube') {
            environment {
                scannerHome = tool 'MaryanScanner'
            }
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh "${scannerHome}/bin/sonar-scanner"
                } 
                echo "${scannerHome}"
            }
        }
    }
}
