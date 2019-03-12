pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            environment {
                scannerHome = tool 'MaryanScanner'
            }
            steps {
                script {
                    withSonarQubeEnv('MaryanSonar') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                    echo "this try"
                }       
            }
        }
    }
}
