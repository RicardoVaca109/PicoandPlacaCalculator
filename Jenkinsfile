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
        DOCKER_IMAGE = "ricardovaca109/pico-placa"
        DOCKER_CREDENTIALS_ID = "docker_hub_credentials"
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
                echo "Analizando estilo de código con flake8..."
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
                    call %VENV_DIR%\\Scripts\\activate
                    pytest --maxfail=1 --disable-warnings --junitxml=reports/junit.xml
                """
            }
        }

        stage('Build') {
            steps {
                echo "Compilando / preparando la app..."
                bat 'echo Build completado exitosamente.'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Construyendo imagen Docker..."
                script {
                    def imageTag = "${env.BUILD_NUMBER}"
                    bat """
                        docker build -t ${DOCKER_IMAGE}:${imageTag} .
                        docker tag ${DOCKER_IMAGE}:${imageTag} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "Subiendo imagen a Docker Hub..."
                script {
                    def imageTag = "${env.BUILD_NUMBER}"
                    withCredentials([usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS_ID}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        bat """
                            echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                            docker push ${DOCKER_IMAGE}:${imageTag}
                            docker push ${DOCKER_IMAGE}:latest
                        """
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "Desplegando aplicación local..."
                bat """
                    if not exist "%REMOTE_PATH%" mkdir "%REMOTE_PATH%"
                    xcopy "*.*" "%REMOTE_PATH%\\" /E /I /Y /EXCLUDE:exclude.txt
                """
            }
        }

        stage('Run App (Temporal)') {
            steps {
                echo "Ejecutando app.py por 1 minuto..."
                bat '''
                cd "%REMOTE_PATH%"

                REM Crear virtualenv si no existe
                if not exist ".venv" (
                    python -m venv .venv
                )

                REM Activar entorno virtual
                call .venv\\Scripts\\activate

                REM Instalar dependencias
                pip install --upgrade pip
                pip install -r requirements.txt

                REM Iniciar app en background
                start /B python app.py

                REM Esperar 5 segundos para que inicie
                ping -n 6 127.0.0.1

                REM Verificar puerto
                netstat -ano | findstr ":5000"

                REM Mantener la app corriendo 60 segundos
                ping -n 61 127.0.0.1

                REM Detener la app
                for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000"') do (
                    if NOT %%a==0 (
                        echo Terminando proceso con PID %%a
                        taskkill /PID %%a /F
                    )
                )
                '''
            }
        }

        stage('Fetch All Branches') {
            steps {
                echo "Descargando todas las ramas del repositorio..."
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '**']],
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
                branch 'dev'
            }
            steps {
                echo "Haciendo merge de dev a master..."
                withCredentials([string(credentialsId: "${GIT_CREDENTIALS_ID}", variable: 'GIT_TOKEN')]) {
                    bat """
                        git config --global user.name "ricardo.vaca"
                        git config --global user.email "ricardo.vaca@udla.edu.ec"
                        git remote set-url origin https://RicardoVaca109:%GIT_TOKEN%@github.com/RicardoVaca109/PicoandPlacaCalculator.git

                        git fetch origin +refs/heads/*:refs/remotes/origin/*

                        git checkout -B master origin/master
                        git checkout -B dev origin/dev

                        git checkout master
                        git merge dev --no-edit

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
                def color = (buildStatus == 'SUCCESS') ? 65280 : 16711680
                def message = "Jenkins Pipeline Report\\n" +
                              "**Proyecto:** ${env.JOB_NAME}\\n" +
                              "**Build:** #${env.BUILD_NUMBER}\\n" +
                              "**Estado:** ${buildStatus}\\n" +
                              "**Repositorio:** ${env.GIT_URL ?: 'No disponible'}\\n" +
                              "**Rama:** ${env.GIT_BRANCH ?: 'No disponible'}\\n" +
                              "**Log:** ${env.BUILD_URL}"

                echo "Enviando notificación a Discord..."

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
