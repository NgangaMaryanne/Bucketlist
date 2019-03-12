pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            environment {
                scannerHome = tool 'MaryanScanner'
            }
            steps {
                
                echo "${scannerHome}"
            }
        }
    }
}
