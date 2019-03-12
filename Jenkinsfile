pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                script {
                    def scannerHome = tool 'MaryanScanner';
                    withSonarQubeEnv('MaryanSonar') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                    echo "this try"
                }       
            }
        }
    }
}
