#!/usr/bin/env python3
"""
NutriApp360 - Script de Instalação Automática
Este script configura automaticamente o ambiente do NutriApp360
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path

def print_banner():
    """Exibe banner do sistema"""
    print("="*60)
    print("         NutriApp360 - Instalação Automática")
    print("         Sistema Completo de Gestão Nutricional")
    print("                    Versão 1.0.0")
    print("="*60)
    print()

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print("1. Verificando versão do Python...")
    
    if sys.version_info < (3, 8):
        print(f"   ERRO: Python 3.8 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"   OK: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def create_directory_structure():
    """Cria estrutura de diretórios necessária"""
    print("2. Criando estrutura de diretórios...")
    
    directories = [
        'data',
        'modules', 
        '.streamlit',
        'backups',
        'logs',
        'uploads'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   Criado: {directory}/")
    
    print("   OK: Estrutura de diretórios criada")

def install_dependencies():
    """Instala dependências Python"""
    print("3. Instalando dependências...")
    
    try:
        # Verificar se pip está disponível
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Atualizar pip
        print("   Atualizando pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Instalar dependências
        print("   Instalando pacotes...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("   OK: Dependências instaladas")
        return True
        
    except subprocess.CalledProcessError:
        print("   ERRO: Falha ao instalar dependências")
        return False
    except FileNotFoundError:
        print("   ERRO: Arquivo requirements.txt não encontrado")
        return False

def create_initial_data():
    """Cria arquivos de dados iniciais"""
    print("4. Criando dados iniciais...")
    
    # Dados de usuários padrão
    if not os.path.exists('data/users.json'):
        default_users = {
            "admin": {
                "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # admin123
                "user_type": "admin",
                "profile": {
                    "nome_completo": "Administrador do Sistema",
                    "email": "admin@nutriapp360.com"
                },
                "created_at": "2024-09-04T10:00:00",
                "status": "ativo"
            }
        }
        
        with open('data/users.json', 'w', encoding='utf-8') as f:
            json.dump(default_users, f, indent=2, ensure_ascii=False)
        print("   Criado: data/users.json")
    
    # Arquivos vazios necessários
    empty_files = [
        'data/patients.json',
        'data/appointments.json', 
        'data/meal_plans.json',
        'data/food_diary.json',
        'data/system_logs.json'
    ]
    
    for file_path in empty_files:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            print(f"   Criado: {file_path}")
    
    print("   OK: Dados iniciais criados")

def create_streamlit_config():
    """Cria configuração do Streamlit"""
    print("5. Configurando Streamlit...")
    
    config_content = """[server]
port = 8501
headless = false
enableCORS = false

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false
serverAddress = "localhost"

[global]
developmentMode = false
logLevel = "info"
"""
    
    with open('.streamlit/config.toml', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("   OK: Configuração do Streamlit criada")

def create_run_script():
    """Cria script de execução"""
    print("6. Criando script de execução...")
    
    system = platform.system().lower()
    
    if system == "windows":
        # Script para Windows
        run_script = """@echo off
echo Iniciando NutriApp360...
echo.
echo Aguarde, o sistema abrirá automaticamente no navegador
echo Para parar o sistema, pressione Ctrl+C
echo.
python -m streamlit run main.py
pause
"""
        with open('run.bat', 'w', encoding='utf-8') as f:
            f.write(run_script)
        print("   Criado: run.bat (Windows)")
    
    else:
        # Script para Unix/Linux/Mac
        run_script = """#!/bin/bash
echo "Iniciando NutriApp360..."
echo ""
echo "Aguarde, o sistema abrirá automaticamente no navegador"
echo "Para parar o sistema, pressione Ctrl+C"
echo ""
python3 -m streamlit run main.py
"""
        with open('run.sh', 'w', encoding='utf-8') as f:
            f.write(run_script)
        
        # Tornar executável
        os.chmod('run.sh', 0o755)
        print("   Criado: run.sh (Unix/Linux/Mac)")

def verify_installation():
    """Verifica se a instalação foi bem-sucedida"""
    print("7. Verificando instalação...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'data/users.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("   ERRO: Arquivos obrigatórios ausentes:")
        for file_path in missing_files:
            print(f"     - {file_path}")
        return False
    
    # Testar importação do Streamlit
    try:
        import streamlit
        print(f"   OK: Streamlit {streamlit.__version__} instalado")
    except ImportError:
        print("   ERRO: Streamlit não foi instalado corretamente")
        return False
    
    print("   OK: Instalação verificada com sucesso")
    return True

def show_completion_message():
    """Exibe mensagem de conclusão"""
    print()
    print("="*60)
    print("           INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print()
    print("Para iniciar o NutriApp360:")
    print()
    
    system = platform.system().lower()
    if system == "windows":
        print("   1. Execute: run.bat")
        print("   2. Ou digite: python -m streamlit run main.py")
    else:
        print("   1. Execute: ./run.sh")
        print("   2. Ou digite: python3 -m streamlit run main.py")
    
    print()
    print("Credenciais padrão:")
    print("   Usuário: admin")
    print("   Senha: admin123")
    print()
    print("IMPORTANTE: Altere a senha padrão após o primeiro acesso!")
    print()
    print("O sistema abrirá automaticamente em: http://localhost:8501")
    print()
    print("Documentação: Consulte README.md para mais informações")
    print("Suporte: nutriapp360@sistema.com")
    print()

def main():
    """Função principal de instalação"""
    print_banner()
    
    # Verificações e instalação
    if not check_python_version():
        sys.exit(1)
    
    create_directory_structure()
    
    if not install_dependencies():
        print("\nERRO: Falha na instalação das dependências")
        print("Tente executar manualmente: pip install -r requirements.txt")
        sys.exit(1)
    
    create_initial_data()
    create_streamlit_config()
    create_run_script()
    
    if not verify_installation():
        print("\nERRO: Verificação da instalação falhou")
        sys.exit(1)
    
    show_completion_message()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstalação interrompida pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERRO INESPERADO: {e}")
        print("Entre em contato com o suporte: nutriapp360@sistema.com")
        sys.exit(1)
