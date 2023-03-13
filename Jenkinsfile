pipeline {
  agent any
  stages {
    stage('Watch Repo') {
      steps {
        git(url: 'https://github.com/tajexume/Micro-Project', branch: 'dev')
      }
    }

    stage('Unit Tests') {
      steps {
        sh 'echo Hello'
      }
    }

    stage('Docker Build') {
      steps {
        sleep 2
      }
    }

    stage('Push Image') {
      steps {
        pwd()
      }
    }

    stage('Start Containers') {
      steps {
        echo 'Starting Container'
      }
    }

  }
}