pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            environment {
                scannerHome = 'opt/sonar-scanner'
            }
            steps {
                sh "${scannerHome}/bin/sonar-scanner"  
            }
        }
    }
}
