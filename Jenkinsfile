pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            environment {
                scannerHome = tool 'Sonarqube Scanner 2.8'
            }
            steps {
                withSonarQubeEnv('MaryanSonar') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
                echo "this try"
            }
        }
    }
}
