pipeline {
    agent any
    stages {
        stage('build') {
            environment {
                SONARQUBE_SERVER = MaryanSonar
                SONAR_HOST_URL = "http://10.0.15.17:9000"
            }
            steps {
                script {
                    def sonnarHome = tool ('MaryanSonar');
                    sh "${sonnarHome}/bin/sonar-scanner"
                }     
            }
        }
    }
}
