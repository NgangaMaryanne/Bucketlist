pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                def scannerHome = tool 'MaryanScanner';
                echo "${scannerHome}"
            }
        }
    }
}
