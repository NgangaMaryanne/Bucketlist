pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                withSonarQubeEnv('MaryanSonar') {
                    sh "/opt/sonar-scanner/bin/sonar-scanner"
                }      
            }
        }
    }
}
