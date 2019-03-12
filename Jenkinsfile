pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                def scannerHome = tool 'SonarQube Scanner 2.8';
                withSonarQubeEnv('MaryanSonar') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
                echo "this try"
            }
        }
    }
}
