pipeline {
    agent any
    stages {
        stage('build') {
            environment {
                SONARQUBE_SERVER = MaryanSonar
                systemProp.sonar.host.url = 'http://10.0.15.17:9000'
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
