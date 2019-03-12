pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            environment {
                scannerHome = tool 'SonarQube Scanner for Jenkins 2.8.1'
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
