pipeline {
    agent none
    stages {
        stage('build') {
            steps {
                script {
                    def sonnarHome = tool ('MaryanScanner');
                    withSonarQubeEnv('MaryanSonar') {
                        sh "${sonnarHome}/bin/sonar-scanner"
                    } 
                }     
            }
        }
    }
}
