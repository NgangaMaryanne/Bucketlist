pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            environment {
                scannerHome = tool 'SonarQube Scanner'
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
