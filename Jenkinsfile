pipeline {
    agent any
    stages {
        stage('build') {
            environment {
                SONARQUBE_SERVER = 'MaryanSonar'
            }
            steps {
                script {
                    def sonnarHome = tool ('MaryanSonar');
                    withSonarQubeEnv(SONARQUBE_SERVER) {
                        sh "${sonnarHome}/bin/sonar-scanner"
                    } 
                }     
            }
        }
    }
}
