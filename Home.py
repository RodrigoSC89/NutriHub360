# NutriApp360 - Sistema Completo de Nutrição
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

# Configuração de cache para melhor performance
@st.cache_data
def load_user_data():
    """Carrega dados dos usuários do arquivo JSON"""
    if os.path.exists('data/users.json'):
        with open('data/users.json', 'r') as f:
            return json.load(f)
    return {}

@st.cache_data
def load_patient_data():
    """Carrega dados dos pacientes"""
    if os.path.exists('data/patients.json'):
        with open('data/patients.json', 'r') as f:
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
                'created_at': datetime.now().isoformat()
            }
            self.save_users()
            return True
        return False
    
    def save_users(self):
        """Salva dados dos usuários"""
        os.makedirs('data', exist_ok=True)
        with open('data/users.json', 'w') as f:
            json.dump(self.users, f, indent=2)

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
    
    def show_login(self):
        """Exibe tela de login"""
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: #4CAF50;'>🥗 NutriApp360</h1>
            <h3>Sistema Completo de Gestão Nutricional</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.container():
                st.markdown("### 🔐 Login")
                
                username = st.text_input("Usuário")
                password = st.text_input("Senha", type="password")
                
                col_login, col_register = st.columns(2)
                
                with col_login:
                    if st.button("Entrar", use_container_width=True):
                        user = self.auth.authenticate(username, password)
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.user = user
                            st.session_state.user['username'] = username
                            st.rerun()
                        else:
                            st.error("Credenciais inválidas!")
                
                with col_register:
                    if st.button("Registrar", use_container_width=True):
                        st.session_state.current_page = 'register'
                        st.rerun()
    
    def show_register(self):
        """Exibe tela de registro"""
        st.markdown("### 📝 Registro de Usuário")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
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
            elif user_type == 'paciente':
                profile_data['nome_completo'] = st.text_input("Nome Completo")
                profile_data['data_nascimento'] = st.date_input("Data de Nascimento")
            
            col_back, col_submit = st.columns(2)
            
            with col_back:
                if st.button("Voltar", use_container_width=True):
                    st.session_state.current_page = 'login'
                    st.rerun()
            
            with col_submit:
                if st.button("Registrar", use_container_width=True):
                    if password != confirm_password:
                        st.error("Senhas não coincidem!")
                    elif len(password) < 6:
                        st.error("Senha deve ter pelo menos 6 caracteres!")
                    elif self.auth.register_user(username, password, user_type, profile_data):
                        st.success("Usuário registrado com sucesso!")
                        st.session_state.current_page = 'login'
                        st.rerun()
                    else:
                        st.error("Usuário já existe!")
    
    def show_sidebar(self):
        """Exibe barra lateral com navegação"""
        user_type = st.session_state.user['user_type']
        username = st.session_state.user['username']
        
        with st.sidebar:
            st.markdown(f"### 👋 Olá, {username}")
            st.markdown(f"**Perfil:** {user_type.replace('_', ' ').title()}")
            
            st.divider()
            
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
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.current_page = 'login'
                st.rerun()
    
    def show_admin_menu(self):
        """Menu para administradores"""
        st.markdown("### 🔧 Administração")
        if st.button("👥 Gestão de Usuários", use_container_width=True):
            st.session_state.current_page = 'user_management'
        if st.button("📊 Analytics do Sistema", use_container_width=True):
            st.session_state.current_page = 'system_analytics'
        if st.button("⚙️ Configurações", use_container_width=True):
            st.session_state.current_page = 'system_config'
    
    def show_nutritionist_menu(self):
        """Menu para nutricionistas"""
        st.markdown("### 🥗 Nutrição")
        if st.button("📋 Dashboard", use_container_width=True):
            st.session_state.current_page = 'nutritionist_dashboard'
        if st.button("👤 Pacientes", use_container_width=True):
            st.session_state.current_page = 'patients'
        if st.button("📅 Agenda", use_container_width=True):
            st.session_state.current_page = 'schedule'
        if st.button("🍽️ Planos Alimentares", use_container_width=True):
            st.session_state.current_page = 'meal_plans'
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
    
    def show_student_menu(self):
        """Menu para estudantes/estagiários"""
        st.markdown("### 📚 Estudos")
        if st.button("📖 Casos de Estudo", use_container_width=True):
            st.session_state.current_page = 'study_cases'
        if st.button("🧮 Calculadoras", use_container_width=True):
            st.session_state.current_page = 'calculators'
        if st.button("🎯 Simulações", use_container_width=True):
            st.session_state.current_page = 'simulations'
    
    def run(self):
        """Executa a aplicação principal"""
        # CSS personalizado
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #4CAF50, #45a049);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
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
            else:
                self.show_default_dashboard()
    
    def show_default_dashboard(self):
        """Dashboard padrão baseado no tipo de usuário"""
        user_type = st.session_state.user['user_type']
        
        st.markdown(f"""
        <div class='main-header'>
            <h1 style='color: white; margin: 0;'>🥗 NutriApp360 - {user_type.replace('_', ' ').title()}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚀 Bem-vindo ao NutriApp360!")
        st.info("Selecione uma opção no menu lateral para começar.")

# Executar aplicação
if __name__ == "__main__":
    app = NutriApp360()
    app.run()