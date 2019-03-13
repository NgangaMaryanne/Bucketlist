pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                def sonnarHome = tool ('MaryanScanner');
                withSonarQubeEnv('MaryanSonar') {
                    sh "${sonnarHome}/bin/sonar-scanner"
                }      
            }
        }
    }
}
