pipeline {
    agent any

    environment {
        APP_NAME = "pico-placa-flask"
        PYTHON = "python"          // Asegúrate que Python esté en PATH
        VENV_DIR = ".venv"
        REMOTE_USER = "ricardo_vaca"
        REMOTE_HOST = "localhost"
        REMOTE_PATH = "C:\\Users\\ricardo_vaca\\app"  // Ajusta ruta de despliegue en Windows
        GIT_CREDENTIALS_ID = "github_token"           // ID del token de GitHub en Jenkins
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
                bat """
                    if not exist "%VENV_DIR%" (
                        %PYTHON% -m venv %VENV_DIR%
                    )
                    call %VENV_DIR%\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Lint') {
            steps {
                echo "🔍 Analizando estilo de código con flake8..."
                bat """
                    call %VENV_DIR%\\Scripts\\activate
                    pip install flake8
                    flake8 .
                """
            }
        }

        stage('Unit Tests') {
            steps {
                echo "🧪 Ejecutando pruebas unitarias..."
                bat """
                    mkdir reports
                    set PYTHONPATH=%cd%
                    call .venv\\Scripts\\activate
                    pytest --maxfail=1 --disable-warnings --junitxml=reports/junit.xml
                """
            }
        }

        stage('Build') {
            steps {
                echo "⚙️ Compilando / preparando la app..."
                bat 'echo Build completado exitosamente.'
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Desplegando aplicación local..."
                bat """
                    REM Copiar archivos al destino (simula deploy)
                    if not exist "%REMOTE_PATH%" mkdir "%REMOTE_PATH%"
                    xcopy "*.*" "%REMOTE_PATH%\\" /E /I /Y /EXCLUDE:.git;.venv
                """
            }
        }

        stage('Push to Main') {
            when {
                branch 'master'
            }
            steps {
                echo "📤 Subiendo cambios a rama main..."
                withCredentials([usernamePassword(credentialsId: "${GIT_CREDENTIALS_ID}", usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    bat """
                        git config user.name "ricardo.vaca"
                        git config user.email "ricardo.vaca@udla.edu.ec"
                        git remote set-url origin https://%GIT_USER%:%GIT_TOKEN%@github.com/%GIT_USER%/%APP_NAME%.git
                        git checkout main || git checkout -b main
                        git merge master --no-edit
                        git push origin main
                    """
                }
            }
        }
    }

    post {
        always {
            echo "📋 Pipeline finalizado (estado: ${currentBuild.currentResult})"
            script {
                // Enviar notificación a GitHub
                def status = currentBuild.currentResult == 'SUCCESS' ? 'success' : 'failure'
                githubNotify context: 'CI/CD Pipeline',
                             description: "Build ${currentBuild.currentResult}",
                             status: status,
                             credentialsId: "${GIT_CREDENTIALS_ID}"
            }
        }
    }
}
