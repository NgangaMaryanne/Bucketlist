pipeline {
    agent any
    stages {
        stage('build') {
            environment {
                SONARQUBE_SERVER = 'MaryanSonar'
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
