pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            environment {
                scannerHome = tool 'MaryanSonar'
            }
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
                echo "this try"
            }
        }
    }
}
