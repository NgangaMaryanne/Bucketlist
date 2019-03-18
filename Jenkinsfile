pipeline {
    agent any
    stages {
        stage('build') {
            environment {
                SONARQUBE_SERVER = 'MaryanSonar'
                SONAR_HOST_URL = "http://10.0.15.17:9000"
                scannerHome = 'opt/sonar-scanner'
            }
            steps {
                sh "make sonarqube"
            }
        }
    }
}
