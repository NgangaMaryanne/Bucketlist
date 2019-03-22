pipeline {
    agent any
    stages {
        stage('build') {
            environment {
                SONARQUBE_SERVER = 'MaryanSonar'
                scannerHome = '/opt/jenkins/sonar-scanner'
                SONAR_HOST_URL = 'http://10.0.15.17:9000'
            }
            steps {
                withSonarQubeEnv(SONARQUBE_SERVER) {
                    sh "make all"
                }
            }
        }
    }
}
