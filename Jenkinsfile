pipeline {
    agent any

    environment {
        APP_NAME = "pico-placa-flask"
        PYTHON = "python3"
        VENV_DIR = ".venv"
        REMOTE_USER = "ricardo_vaca"
        REMOTE_HOST = "localhost"
        REMOTE_PATH = "/home/ricardo_vaca/app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Clonando el repositorio..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo "Configurando entorno virtual..."
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

        stage('Code Linting') {
            steps {
                echo "Ejecutando análisis de estilo con flake8..."
                sh '''
                    . $VENV_DIR/bin/activate
                    pip install flake8
                    flake8 --ignore=E501 .
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Ejecutando tests con pytest..."
                sh '''
                    . $VENV_DIR/bin/activate
                    pip install pytest
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Quality Scan') {
            steps {
                echo "Analizando calidad del código (simulado Sonar)..."
                sh '''
                    echo "Ejecutar sonar-scanner aquí si está configurado"
                '''
            }
        }

        stage('Build') {
            steps {
                echo "Simulando build de la aplicación Flask..."
                sh '''
                    echo "Build completado exitosamente."
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "Desplegando aplicación en localhost..."
                sh '''
                    chmod +x scripts/deploy.sh
                    bash scripts/deploy.sh
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizado (estado: ${currentBuild.currentResult})"
        }
        success {
            echo "✅ Despliegue exitoso!"
        }
        failure {
            echo "❌ El pipeline falló!"
        }
    }
}