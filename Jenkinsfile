pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            environment {
                scannerHome = tool 'MaryanScanner'
                sonar.host.url = 'http://10.0.15.17:9000'
                sonar.projectName = 'FlaskApi'
            }
            steps {
                withSonarQubeEnv('MaryanSonar') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
                timeout(time: 10, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true
                }
                echo "this try"
            }
        }
    }
}
