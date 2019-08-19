pipeline {
    agent none
    environment {
        TEST_VAR = 'TEST'

      	ALLURE_JIRA_ENDPOINT='https://jira.transmit.im/rest/'
      	JIRA_CREDS=credentials('5d20eed2-b193-46d7-a481-ad7c83087122')
      	ALLURE_JIRA_USERNAME='zs'
        ALLURE_JIRA_PASSWORD=credentials('4df47e91-1933-4a1c-87eb-665af3409649')
    }
  tools {
    			allure 'allure'
    			jdk 'OracleJDK8'
  			}

    stages {
        stage("Test") {
            agent {
                docker {
                    image 'harbor.transmit.im/jnr/jenkins-python-runner:v3.7.4'
                    args '-u jenkins:jenkins -v $HOME/tools:/home/jenkins/tools'
                }
            }
             
            environment {
        		TEST_VAR = 'TEST'

      			ALLURE_JIRA_ENDPOINT='https://jira.transmit.im/rest/'
      			JIRA_CREDS=credentials('5d20eed2-b193-46d7-a481-ad7c83087122')
      			ALLURE_JIRA_USERNAME='zs'
        		ALLURE_JIRA_PASSWORD=credentials('4df47e91-1933-4a1c-87eb-665af3409649')
    		}



            steps {
                checkout scm
                withCredentials([string(credentialsId: '290af1a2-da7e-45f6-82f6-2eb25cea54d5', variable: 'password'), usernamePassword(credentialsId: '015ababb-349d-4a69-b151-75770750ea33', passwordVariable: 'admin_password', usernameVariable: 'admin_username')]) {
                    sh "tox -- tests_functional"
                }
            }

            post {
                always{
                    junit allowEmptyResults: true, testResults:"**/logs/*.xml"
                    step([$class: 'XrayImportBuilder', endpointName: '/junit', importFilePath: 'logs/report.xml', importToSameExecution: 'true', projectKey: 'XTE', serverInstance: '0547defe-480c-495e-85a5-1dc19768fb4f', testEnvironments: 'stand-1.transmit.im', testExecKey: 'XTE-499'])
                    allure jdk: 'OracleJDK8', configPath: 'logs/config.yml', includeProperties: true, properties: [[key: 'allure.tests.management.pattern', value: 'https://jira.transmit.im/browse/%s'], [key: 'allure.issues.tracker.pattern', value: 'https://jira.transmit.im/browse/%s'], [key: 'allure.results.directory', value: 'logs/allure-results']], report: 'logs/allure-report', results: [[path: 'logs/allure-results']]

                }
              }
            }
    }


    post {
        success {
            echo "========pipeline executed successfully ========"
        }
        failure {
            echo "========pipeline execution failed========"
        }
    }
}

