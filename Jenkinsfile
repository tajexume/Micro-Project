pipeline {
  agent any
  stages {
    stage('Checkout Repo') {
      steps {
        git(url: 'https://github.com/tajexume/Micro-Project', branch: 'dev')
      }
    }

    stage('') {
      steps {
        sh 'ls'
      }
    }

  }
}