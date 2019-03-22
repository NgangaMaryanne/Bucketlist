pipeline {
    agent any
    stages {
        stage('build') {
            environment {
                SONARQUBE_SERVER = 'Maryan Sonar'
                SONAR_HOST_URL = "10.0.15.17:9000"
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
