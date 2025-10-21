pipeline {
    agent any

    environment {
        APP_NAME = "pico-placa-flask"
        PYTHON = "python3"
        VENV_DIR = ".venv"
        REMOTE_USER = "ricardo_vaca"
        REMOTE_HOST = "localhost"
        REMOTE_PATH = "/home/ricardo_vaca/app"
        GIT_CREDENTIALS_ID = "github_token"  // ID del token de GitHub en Jenkins
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📦 Clonando repositorio..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo "🐍 Configurando entorno virtual..."
                sh '''
                    if [ ! -d "$VENV_DIR" ]; then
                        $PYTHON -m venv $VENV_DIR
                    fi
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo "🔍 Ejecutando flake8..."
                sh '''
                    . $VENV_DIR/bin/activate
                    flake8 .
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo "🧪 Ejecutando pruebas unitarias..."
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest --maxfail=1 --disable-warnings --junitxml=reports/junit.xml
                '''
            }
        }

        stage('Build') {
            steps {
                echo "⚙️ Compilando aplicación Flask..."
                sh 'echo "Build completado exitosamente."'
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Desplegando aplicación en entorno local..."
                sh '''
                    chmod +x scripts/deploy.sh
                    bash scripts/deploy.sh
                '''
            }
        }

        stage('Promote to Master') {
            when {
                branch 'dev'
            }
            steps {
                echo "📤 Promoviendo cambios desde DEV hacia MASTER..."
                withCredentials([usernamePassword(credentialsId: "${GIT_CREDENTIALS_ID}", usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    sh '''
                        git config user.name "Jenkins CI"
                        git config user.email "jenkins@local"
                        git fetch origin
                        git checkout master
                        git merge dev --no-edit
                        git push https://${GIT_USER}:${GIT_TOKEN}@github.com/${GIT_USER}/${APP_NAME}.git master
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "📋 Pipeline finalizado (estado: ${currentBuild.currentResult})"
        }
        success {
            echo "✅ Pipeline exitoso!"
            mail to: 'ricardo.vaca@udla.edu.ec',
                 subject: "✅ Éxito en ${env.JOB_NAME}",
                 body: "El pipeline ${env.JOB_NAME} se ejecutó correctamente.\nRevisa el build: ${env.BUILD_URL}"
        }
        failure {
            echo "❌ Falló el pipeline!"
            mail to: 'ricardo.vaca@udla.edu.ec',
                 subject: "❌ Falla en ${env.JOB_NAME}",
                 body: "El pipeline ${env.JOB_NAME} falló.\nRevisa el build: ${env.BUILD_URL}"
        }
    }
}
