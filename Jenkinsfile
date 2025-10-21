pipeline {
    agent any

    environment {
        APP_NAME = "PicoandPlacaCalculator"
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
                echo "Clonando repositorio..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo "Configurando entorno virtual..."
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
                echo "Analizando estilo de codigo con flake8..."
                bat """
                    call %VENV_DIR%\\Scripts\\activate
                    pip install flake8
                    flake8 .
                """
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Ejecutando pruebas unitarias..."
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
                echo "Desplegando aplicacion local..."
                bat """
                    if not exist "%REMOTE_PATH%" mkdir "%REMOTE_PATH%"
                    xcopy "*.*" "%REMOTE_PATH%\\" /E /I /Y /EXCLUDE:exclude.txt
                """
            }
        }

        stage('Push to Main') {
            when {
                branch 'dev'  // Solo ejecuta este stage si estás en la rama dev
            }
        steps {
            echo "📤 Haciendo merge de dev a master..."
                withCredentials([string(credentialsId: "${GIT_CREDENTIALS_ID}", variable: 'GIT_TOKEN')]) {
                bat """
                    git config user.name "ricardo.vaca"
                    git config user.email "ricardo.vaca@udla.edu.ec"
                    git remote set-url origin https://RicardoVaca109:%GIT_TOKEN%@github.com/RicardoVaca109/PicoandPlacaCalculator.git
                    git checkout master
                    git merge dev --no-edit
                    git push origin master
                """
                }
            }

        }

        post {
        always {
            echo "Pipeline finalizado con estado: ${currentBuild.currentResult}"
            script {
                if (currentBuild.currentResult == 'SUCCESS') {
                    echo "✅ Build completado correctamente"
                } else {
                    echo "❌ Fallo en el pipeline"
                }
                }
            }
        }
    }
}
