pipeline {
    agent any
    stages {
        stage('build') {
            environment {
                SONARQUBE_SERVER = 'Maryan Sonar'
                scannerHome = '/opt/jenkins/sonar-scanner'
            }
            steps {
                withSonarQubeEnv(SONARQUBE_SERVER) {
                    sh "make all"
                }
            }
        }
    }
}
