pipeline {
    agent any

    environment {
        APP_NAME = "PicoandPlacaCalculator"
        PYTHON = "python"          
        VENV_DIR = ".venv"
        REMOTE_USER = "ricardo_vaca"
        REMOTE_HOST = "localhost"
        REMOTE_PATH = "C:\\Users\\ricardo_vaca\\app"  
        GIT_CREDENTIALS_ID = "github_token"           
        DISCORD_CREDENTIALS_ID = "discord_webhook_url"
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

        stage('Fetch All Branches') {
            steps {
                echo "🔄 Descargando todas las ramas del repositorio..."
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '**']],  // Trae todas las ramas
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/RicardoVaca109/PicoandPlacaCalculator.git',
                        credentialsId: "${GIT_CREDENTIALS_ID}"
                    ]]
                ])
            }
        }

        stage('Push to Master') {
            when {
                branch 'dev'  // Solo ejecuta este stage si estás en la rama dev
            }
            steps {
                echo "📤 Haciendo merge de dev a master..."
                withCredentials([string(credentialsId: "${GIT_CREDENTIALS_ID}", variable: 'GIT_TOKEN')]) {
                    bat """
                        git config --global user.name "ricardo.vaca"
                        git config --global user.email "ricardo.vaca@udla.edu.ec"
                        git remote set-url origin https://RicardoVaca109:%GIT_TOKEN%@github.com/RicardoVaca109/PicoandPlacaCalculator.git

                        REM 🔄 Traer todas las ramas remotas y sus refs
                        git fetch origin +refs/heads/*:refs/remotes/origin/*

                        REM 🔧 Crear o resetear ramas locales a partir de las remotas
                        git checkout -B master origin/master
                        git checkout -B dev origin/dev

                        REM 📥 Cambiar a master y hacer merge
                        git checkout master
                        git merge dev --no-edit

                        REM 📤 Subir cambios a GitHub
                        git push origin master
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizado con estado: ${currentBuild.currentResult}"

            script {
                def buildStatus = currentBuild.currentResult
                def color = (buildStatus == 'SUCCESS') ? 65280 : 16711680  // Verde o rojo
                def message = "🚀 Jenkins Pipeline Report\\n" +
                              "**Proyecto:** ${env.JOB_NAME}\\n" +
                              "**Build:** #${env.BUILD_NUMBER}\\n" +
                              "**Estado:** ${buildStatus}\\n" +
                              "**Repositorio:** ${env.GIT_URL ?: 'No disponible'}\\n" +
                              "**Rama:** ${env.GIT_BRANCH ?: 'No disponible'}\\n" +
                              "**Log:** ${env.BUILD_URL}"

                echo "Enviando notificación a Discord..."

                // 📢 Enviar mensaje a Discord usando credencial segura
                withCredentials([string(credentialsId: "${DISCORD_CREDENTIALS_ID}", variable: 'DISCORD_WEBHOOK')]) {
                    bat """
                        curl -H "Content-Type: application/json" ^
                             -X POST ^
                             -d "{\\"embeds\\":[{\\"title\\":\\"${env.JOB_NAME}\\",\\"description\\":\\"${message}\\",\\"color\\":${color}}]}" ^
                             %DISCORD_WEBHOOK%
                    """
                }
            }
        }
    }
}
