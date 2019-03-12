pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            withSonarQubeEnv('My SonarQube Server') {
                sh "/opt/sonar-scanner/bin/sonar-scanner"
            }
            steps {
                echo "this try"
                sh './build.sh'
            }
        }
    }
}
