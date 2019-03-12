pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            def scannerHome = tool 'SonarQube Scanner 2.8';
            withSonarQubeEnv('My SonarQube Server') {
                sh "${scannerHome}/bin/sonar-scanner"
            }
            steps {
                echo "this try"
                sh './build.sh'
            }
        }
    }
}
