# NutriApp360 - Sistema Completo de Gestão Nutricional
# Arquivo principal: main.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import json
import os
from typing import Dict, List, Optional

# Configuração da página
st.set_page_config(
    page_title="NutriApp360",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Garantir que diretórios existem
def ensure_directories():
    """Garante que os diretórios necessários existem"""
    directories = ['data', 'modules', '.streamlit', 'backups']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Inicializar dados padrão
def init_default_data():
    """Inicializa dados padrão se não existirem"""
    ensure_directories()
    
    # Criar usuário admin padrão
    users_file = 'data/users.json'
    if not os.path.exists(users_file):
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
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(default_users, f, indent=2, ensure_ascii=False)
    
    # Criar arquivos vazios se não existirem
    empty_files = ['data/patients.json', 'data/appointments.json', 'data/meal_plans.json']
    for file_path in empty_files:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)

# Configuração de cache para melhor performance
@st.cache_data
def load_user_data():
    """Carrega dados dos usuários do arquivo JSON"""
    if os.path.exists('data/users.json'):
        with open('data/users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@st.cache_data
def load_patient_data():
    """Carrega dados dos pacientes"""
    if os.path.exists('data/patients.json'):
        with open('data/patients.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Sistema de autenticação
class AuthSystem:
    def __init__(self):
        self.users = load_user_data()
    
    def hash_password(self, password: str) -> str:
        """Cria hash da senha para segurança"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Autentica usuário e retorna seus dados"""
        if username in self.users:
            user_data = self.users[username]
            if user_data['password'] == self.hash_password(password):
                return user_data
        return None
    
    def register_user(self, username: str, password: str, user_type: str, profile_data: Dict):
        """Registra novo usuário"""
        if username not in self.users:
            self.users[username] = {
                'password': self.hash_password(password),
                'user_type': user_type,
                'profile': profile_data,
                'created_at': datetime.now().isoformat(),
                'status': 'ativo'
            }
            self.save_users()
            return True
        return False
    
    def save_users(self):
        """Salva dados dos usuários"""
        os.makedirs('data', exist_ok=True)
        with open('data/users.json', 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=2, ensure_ascii=False)

# Sistema de permissões
class PermissionSystem:
    PERMISSIONS = {
        'admin': [
            'manage_users', 'view_all_data', 'system_config', 
            'financial_reports', 'audit_logs', 'backup_restore'
        ],
        'nutricionista_senior': [
            'manage_patients', 'create_protocols', 'supervise_team',
            'advanced_reports', 'edit_templates', 'view_statistics'
        ],
        'nutricionista_pleno': [
            'manage_patients', 'create_meal_plans', 'basic_reports',
            'patient_communication', 'scheduling'
        ],
        'nutricionista_junior': [
            'view_patients', 'create_meal_plans_supervised', 
            'basic_reports', 'patient_communication'
        ],
        'estagiario': [
            'view_cases_anonymous', 'educational_content', 
            'calculators', 'simulations'
        ],
        'recepcionista': [
            'scheduling', 'patient_registration', 'financial_basic',
            'administrative_reports'
        ],
        'paciente': [
            'view_own_plan', 'food_diary', 'schedule_appointments',
            'chat_nutritionist', 'view_own_progress'
        ]
    }
    
    @staticmethod
    def has_permission(user_type: str, permission: str) -> bool:
        """Verifica se usuário tem permissão específica"""
        return permission in PermissionSystem.PERMISSIONS.get(user_type, [])

# Decorador para controle de acesso
def require_permission(permission: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'user' not in st.session_state:
                st.error("Acesso negado. Faça login primeiro.")
                return None
            
            user_type = st.session_state.user['user_type']
            if not PermissionSystem.has_permission(user_type, permission):
                st.error(f"Acesso negado. Permissão '{permission}' necessária.")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Classe principal da aplicação
class NutriApp360:
    def __init__(self):
        init_default_data()
        self.auth = AuthSystem()
        self.init_session_state()
    
    def init_session_state(self):
        """Inicializa estados da sessão"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'login'
        if 'show_patient_form' not in st.session_state:
            st.session_state.show_patient_form = False
        if 'show_meal_plan_form' not in st.session_state:
            st.session_state.show_meal_plan_form = False
    
    def show_login(self):
        """Exibe tela de login"""
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: #4CAF50; font-size: 3rem; margin-bottom: 0;'>🥗 NutriApp360</h1>
            <h3 style='color: #666; margin-top: 0;'>Sistema Completo de Gestão Nutricional</h3>
            <p style='color: #888;'>Versão 1.0.0 - Desenvolvido para profissionais de nutrição</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.container():
                st.markdown("""
                <div style='background: white; padding: 2rem; border-radius: 10px; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border: 1px solid #e0e0e0;'>
                """, unsafe_allow_html=True)
                
                st.markdown("### 🔐 Acesso ao Sistema")
                
                username = st.text_input("👤 Usuário", placeholder="Digite seu nome de usuário")
                password = st.text_input("🔑 Senha", type="password", placeholder="Digite sua senha")
                
                # Informações de acesso padrão
                with st.expander("ℹ️ Informações de Acesso"):
                    st.markdown("""
                    **Usuário padrão:**
                    - **Usuário:** `admin`
                    - **Senha:** `admin123`
                    
                    **⚠️ Importante:** Altere a senha padrão após o primeiro acesso.
                    """)
                
                col_login, col_register = st.columns(2)
                
                with col_login:
                    if st.button("🚀 Entrar", use_container_width=True, type="primary"):
                        if not username or not password:
                            st.error("⚠️ Por favor, preencha todos os campos.")
                        else:
                            user = self.auth.authenticate(username, password)
                            if user:
                                st.session_state.authenticated = True
                                st.session_state.user = user
                                st.session_state.user['username'] = username
                                st.success("✅ Login realizado com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Credenciais inválidas!")
                
                with col_register:
                    if st.button("📝 Registrar", use_container_width=True):
                        st.session_state.current_page = 'register'
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    def show_register(self):
        """Exibe tela de registro"""
        st.markdown("### 📝 Registro de Usuário")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("register_form"):
                username = st.text_input("Nome de Usuário")
                password = st.text_input("Senha", type="password")
                confirm_password = st.text_input("Confirmar Senha", type="password")
                
                user_type = st.selectbox("Tipo de Usuário", [
                    'paciente', 'nutricionista_junior', 'nutricionista_pleno', 
                    'nutricionista_senior', 'estagiario', 'recepcionista'
                ])
                
                # Campos específicos por tipo de usuário
                profile_data = {}
                if user_type.startswith('nutricionista'):
                    profile_data['crn'] = st.text_input("CRN")
                    profile_data['especialidade'] = st.text_input("Especialidade")
                    profile_data['nome_completo'] = st.text_input("Nome Completo")
                elif user_type == 'paciente':
                    profile_data['nome_completo'] = st.text_input("Nome Completo")
                    profile_data['data_nascimento'] = st.date_input("Data de Nascimento").isoformat()
                else:
                    profile_data['nome_completo'] = st.text_input("Nome Completo")
                
                profile_data['email'] = st.text_input("E-mail")
                
                col_back, col_submit = st.columns(2)
                
                with col_back:
                    back_button = st.form_submit_button("⬅️ Voltar", use_container_width=True)
                
                with col_submit:
                    submit_button = st.form_submit_button("✅ Registrar", use_container_width=True, type="primary")
                
                if back_button:
                    st.session_state.current_page = 'login'
                    st.rerun()
                
                if submit_button:
                    if password != confirm_password:
                        st.error("❌ Senhas não coincidem!")
                    elif len(password) < 6:
                        st.error("❌ Senha deve ter pelo menos 6 caracteres!")
                    elif self.auth.register_user(username, password, user_type, profile_data):
                        st.success("✅ Usuário registrado com sucesso!")
                        st.session_state.current_page = 'login'
                        st.rerun()
                    else:
                        st.error("❌ Usuário já existe!")
    
    def show_sidebar(self):
        """Exibe barra lateral com navegação"""
        user_type = st.session_state.user['user_type']
        username = st.session_state.user['username']
        
        with st.sidebar:
            st.markdown(f"""
            <div style='background: linear-gradient(90deg, #4CAF50, #45a049); 
            padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;'>
                <h3 style='color: white; margin: 0;'>👋 Olá, {username}</h3>
                <p style='color: white; margin: 0; opacity: 0.9;'>{user_type.replace('_', ' ').title()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Menu baseado no tipo de usuário
            if user_type == 'admin':
                self.show_admin_menu()
            elif user_type.startswith('nutricionista'):
                self.show_nutritionist_menu()
            elif user_type == 'paciente':
                self.show_patient_menu()
            elif user_type == 'recepcionista':
                self.show_receptionist_menu()
            elif user_type == 'estagiario':
                self.show_student_menu()
            
            st.divider()
            
            # Botão de logout
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.current_page = 'login'
                st.rerun()
            
            # Footer
            st.markdown("""
            ---
            <div style='text-align: center; opacity: 0.6; font-size: 0.8rem;'>
                <p>NutriApp360 v1.0.0<br>© 2024 Sistema de Nutrição</p>
            </div>
            """, unsafe_allow_html=True)
    
    def show_admin_menu(self):
        """Menu para administradores"""
        st.markdown("### 🔧 Administração")
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.current_page = 'admin_dashboard'
        if st.button("👥 Gestão de Usuários", use_container_width=True):
            st.session_state.current_page = 'user_management'
        if st.button("⚙️ Configurações", use_container_width=True):
            st.session_state.current_page = 'system_config'
        if st.button("📋 Logs do Sistema", use_container_width=True):
            st.session_state.current_page = 'system_logs'
        if st.button("💾 Backup", use_container_width=True):
            st.session_state.current_page = 'backup_restore'
    
    def show_nutritionist_menu(self):
        """Menu para nutricionistas"""
        st.markdown("### 🥗 Nutrição")
        if st.button("📋 Dashboard", use_container_width=True):
            st.session_state.current_page = 'nutritionist_dashboard'
        if st.button("👤 Pacientes", use_container_width=True):
            st.session_state.current_page = 'patients'
        if st.button("🍽️ Planos Alimentares", use_container_width=True):
            st.session_state.current_page = 'meal_plans'
        if st.button("🧮 Calculadoras", use_container_width=True):
            st.session_state.current_page = 'calculators'
        if st.button("📅 Agenda", use_container_width=True):
            st.session_state.current_page = 'schedule'
        if st.button("📈 Relatórios", use_container_width=True):
            st.session_state.current_page = 'reports'
    
    def show_patient_menu(self):
        """Menu para pacientes"""
        st.markdown("### 🏠 Minha Área")
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.current_page = 'patient_dashboard'
        if st.button("🍽️ Meu Plano", use_container_width=True):
            st.session_state.current_page = 'my_plan'
        if st.button("📝 Diário Alimentar", use_container_width=True):
            st.session_state.current_page = 'food_diary'
        if st.button("📅 Consultas", use_container_width=True):
            st.session_state.current_page = 'my_appointments'
        if st.button("💬 Chat", use_container_width=True):
            st.session_state.current_page = 'chat'
    
    def show_receptionist_menu(self):
        """Menu para recepcionistas"""
        st.markdown("### 📋 Recepção")
        if st.button("📅 Agendamentos", use_container_width=True):
            st.session_state.current_page = 'scheduling'
        if st.button("👤 Cadastros", use_container_width=True):
            st.session_state.current_page = 'registrations'
        if st.button("💰 Financeiro", use_container_width=True):
            st.session_state.current_page = 'financial'
        if st.button("📊 Relatórios", use_container_width=True):
            st.session_state.current_page = 'reports'
    
    def show_student_menu(self):
        """Menu para estudantes/estagiários"""
        st.markdown("### 📚 Estudos")
        if st.button("📖 Casos de Estudo", use_container_width=True):
            st.session_state.current_page = 'study_cases'
        if st.button("🧮 Calculadoras", use_container_width=True):
            st.session_state.current_page = 'calculators'
        if st.button("🎯 Simulações", use_container_width=True):
            st.session_state.current_page = 'simulations'
        if st.button("📚 Biblioteca", use_container_width=True):
            st.session_state.current_page = 'library'
    
    def run(self):
        """Executa a aplicação principal"""
        # CSS personalizado
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #4CAF50, #45a049);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #4CAF50;
        }
        .success-alert {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 0.75rem 1.25rem;
            border-radius: 0.25rem;
            margin-bottom: 1rem;
        }
        .stButton > button {
            border-radius: 8px;
            border: none;
            font-weight: 500;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        if not st.session_state.authenticated:
            if st.session_state.current_page == 'register':
                self.show_register()
            else:
                self.show_login()
        else:
            self.show_sidebar()
            
            # Roteamento de páginas
            current_page = st.session_state.get('current_page', 'dashboard')
            
            try:
                # Importar e mostrar módulos específicos
                if current_page == 'nutritionist_dashboard':
                    from modules.nutritionist_dashboard import show_nutritionist_dashboard
                    show_nutritionist_dashboard()
                elif current_page == 'patient_dashboard':
                    from modules.patient_dashboard import show_patient_dashboard
                    show_patient_dashboard()
                elif current_page == 'patients':
                    from modules.patient_management import show_patient_management
                    show_patient_management()
                elif current_page == 'meal_plans':
                    from modules.meal_plans import show_meal_plans
                    show_meal_plans()
                elif current_page == 'calculators':
                    from modules.calculators import show_calculators
                    show_calculators()
                elif current_page in ['admin_dashboard', 'user_management', 'system_config', 'system_logs', 'backup_restore']:
                    from modules.admin_config import show_admin_dashboard
                    show_admin_dashboard()
                else:
                    self.show_default_dashboard()
            except ImportError as e:
                st.error(f"❌ Erro ao carregar módulo: {e}")
                st.info("📁 Verifique se todos os arquivos estão na pasta 'modules/'")
                self.show_default_dashboard()
    
    def show_default_dashboard(self):
        """Dashboard padrão baseado no tipo de usuário"""
        user_type = st.session_state.user['user_type']
        user_name = st.session_state.user.get('username', 'Usuário')
        
        st.markdown(f"""
        <div class='main-header'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🥗 NutriApp360</h1>
            <h2 style='color: white; margin: 0.5rem 0 0 0; opacity: 0.9;'>
                {user_type.replace('_', ' ').title()}
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"### 🚀 Bem-vindo ao sistema, {user_name}!")
        
        # Informações baseadas no tipo de usuário
        if user_type == 'admin':
            st.info("👑 Como administrador, você tem acesso completo ao sistema. Use o menu lateral para gerenciar usuários, configurações e realizar backups.")
        elif user_type.startswith('nutricionista'):
            st.info("🥗 Como nutricionista, você pode gerenciar pacientes, criar planos alimentares e acompanhar a evolução dos tratamentos.")
        elif user_type == 'paciente':
            st.info("👤 Como paciente, você pode acompanhar seu plano alimentar, registrar seu diário e comunicar-se com seu nutricionista.")
        elif user_type == 'recepcionista':
            st.info("📋 Como recepcionista, você pode gerenciar agendamentos, cadastros e relatórios administrativos.")
        elif user_type == 'estagiario':
            st.info("📚 Como estagiário, você tem acesso a casos de estudo, calculadoras e conteúdo educacional.")
        
        # Ações rápidas
        st.markdown("### ⚡ Ações Rápidas")
        
        col1, col2, col3, col4 = st.columns(4)
        
        if user_type.startswith('nutricionista') or user_type == 'admin':
            with col1:
                if st.button("👤 Pacientes", use_container_width=True):
                    st.session_state.current_page = 'patients'
                    st.rerun()
            with col2:
                if st.button("🍽️ Planos", use_container_width=True):
                    st.session_state.current_page = 'meal_plans'
                    st.rerun()
            with col3:
                if st.button("🧮 Calculadoras", use_container_width=True):
                    st.session_state.current_page = 'calculators'
                    st.rerun()
            with col4:
                if st.button("📊 Dashboard", use_container_width=True):
                    st.session_state.current_page = 'nutritionist_dashboard'
                    st.rerun()
        
        # Informações sobre o sistema
        with st.expander("ℹ️ Sobre o NutriApp360"):
            st.markdown("""
            **NutriApp360** é um sistema completo de gestão nutricional que oferece:
            
            - 👥 **Gestão de Pacientes** - Cadastro e acompanhamento completo
            - 🍽️ **Planos Alimentares** - Criação personalizada com cálculos nutricionais
            - 🧮 **Calculadoras** - TMB, IMC, macronutrientes e mais
            - 📊 **Dashboards** - Acompanhamento visual de progresso
            - 🔐 **Sistema de Permissões** - Acesso controlado por perfil
            - 💾 **Backup Automático** - Segurança dos dados
            
            **Versão:** 1.0.0  
            **Suporte:** nutriapp360@sistema.com
            """)

# Executar aplicação
if __name__ == "__main__":
    app = NutriApp360()
    app.run()