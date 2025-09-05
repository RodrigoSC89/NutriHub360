# modules/admin_config.py
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

class AdminManager:
    def __init__(self):
        self.config_file = 'data/system_config.json'
        self.logs_file = 'data/system_logs.json'
        self.backup_dir = 'backups'
        self.ensure_directories()
        self.init_config()
    
    def ensure_directories(self):
        """Garante que os diretórios necessários existem"""
        os.makedirs('data', exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def init_config(self):
        """Inicializa configurações padrão se não existirem"""
        if not os.path.exists(self.config_file):
            default_config = {
                "system_name": "NutriApp360",
                "version": "1.0.0",
                "max_users": 100,
                "session_timeout": 30,
                "backup_frequency": "daily",
                "email_notifications": True,
                "maintenance_mode": False,
                "default_language": "pt-BR",
                "theme": "light",
                "features": {
                    "patient_portal": True,
                    "mobile_app": True,
                    "reports": True,
                    "integrations": False,
                    "advanced_analytics": False
                },
                "security": {
                    "password_min_length": 6,
                    "session_encryption": True,
                    "two_factor_auth": False,
                    "login_attempts": 3
                }
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    @st.cache_data
    def load_config(_self):
        """Carrega configurações do sistema"""
        with open(_self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_config(self, config):
        """Salva configurações do sistema"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # Log da alteração
        self.log_action("config_updated", "Configurações do sistema atualizadas")
    
    def log_action(self, action_type, description, user_id="system"):
        """Registra ação no log do sistema"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action_type": action_type,
            "description": description
        }
        
        # Carregar logs existentes
        logs = []
        if os.path.exists(self.logs_file):
            with open(self.logs_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        # Manter apenas os últimos 1000 logs
        if len(logs) > 1000:
            logs = logs[-1000:]
        
        # Salvar logs
        with open(self.logs_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False, default=str)
    
    @st.cache_data
    def get_system_stats(_self):
        """Obtém estatísticas do sistema"""
        stats = {
            "total_users": 0,
            "active_users": 0,
            "total_patients": 0,
            "total_plans": 0,
            "total_appointments": 0,
            "disk_usage": "125 MB",
            "uptime": "15 dias, 3 horas",
            "last_backup": "2024-09-04 03:00:00"
        }
        
        # Simular carregamento de dados reais
        if os.path.exists('data/users.json'):
            with open('data/users.json', 'r') as f:
                users = json.load(f)
                stats["total_users"] = len(users)
                stats["active_users"] = len([u for u in users.values() if u.get('status') != 'inactive'])
        
        if os.path.exists('data/patients.json'):
            with open('data/patients.json', 'r') as f:
                patients = json.load(f)
                stats["total_patients"] = len(patients)
        
        if os.path.exists('data/meal_plans.json'):
            with open('data/meal_plans.json', 'r') as f:
                plans = json.load(f)
                stats["total_plans"] = len(plans)
        
        return stats

def show_system_overview():
    """Exibe visão geral do sistema"""
    st.markdown("### 🖥️ Visão Geral do Sistema")
    
    admin = AdminManager()
    stats = admin.get_system_stats()
    
    # Métricas principais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Usuários Totais", stats["total_users"])
    
    with col2:
        st.metric("Usuários Ativos", stats["active_users"])
    
    with col3:
        st.metric("Pacientes", stats["total_patients"])
    
    with col4:
        st.metric("Planos Criados", stats["total_plans"])
    
    with col5:
        st.metric("Consultas", stats["total_appointments"])
    
    # Informações do sistema
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💾 Recursos do Sistema")
        st.write(f"**Uso de disco:** {stats['disk_usage']}")
        st.write(f"**Tempo ativo:** {stats['uptime']}")
        st.write(f"**Último backup:** {stats['last_backup']}")
        
        # Status dos serviços
        services = [
            {"name": "API Principal", "status": "🟢 Online"},
            {"name": "Banco de Dados", "status": "🟢 Online"},
            {"name": "Sistema de Backup", "status": "🟢 Online"},
            {"name": "Notificações", "status": "🟡 Degradado"},
            {"name": "Relatórios", "status": "🟢 Online"}
        ]
        
        st.markdown("#### 🔧 Status dos Serviços")
        for service in services:
            st.write(f"**{service['name']}:** {service['status']}")
    
    with col2:
        # Gráfico de uso por tipo de usuário
        user_types = ["Nutricionistas", "Pacientes", "Recepcionistas", "Administradores"]
        user_counts = [12, 45, 3, 2]
        
        fig = px.pie(
            values=user_counts,
            names=user_types,
            title="Distribuição de Usuários por Tipo",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_user_management():
    """Gestão de usuários"""
    st.markdown("### 👥 Gestão de Usuários")
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_type = st.selectbox("Tipo de Usuário", 
                                  ["Todos", "admin", "nutricionista_senior", "nutricionista_pleno", 
                                   "nutricionista_junior", "paciente", "recepcionista", "estagiario"])
    
    with col2:
        filter_status = st.selectbox("Status", ["Todos", "Ativo", "Inativo", "Suspenso"])
    
    with col3:
        search_user = st.text_input("🔍 Buscar usuário")
    
    with col4:
        if st.button("➕ Novo Usuário", use_container_width=True):
            st.session_state.show_new_user_form = True
    
    # Lista de usuários (simulada)
    users_data = [
        {"id": "001", "username": "admin", "name": "Administrador", "type": "admin", "status": "Ativo", "last_login": "2024-09-04 09:30"},
        {"id": "002", "username": "dr.ana", "name": "Dr. Ana Silva", "type": "nutricionista_senior", "status": "Ativo", "last_login": "2024-09-04 08:15"},
        {"id": "003", "username": "nutri.carlos", "name": "Carlos Santos", "type": "nutricionista_pleno", "status": "Ativo", "last_login": "2024-09-03 17:45"},
        {"id": "004", "username": "maria.silva", "name": "Maria Silva", "type": "paciente", "status": "Ativo", "last_login": "2024-09-04 07:20"},
        {"id": "005", "username": "recep.lucia", "name": "Lúcia Costa", "type": "recepcionista", "status": "Ativo", "last_login": "2024-09-04 09:00"}
    ]
    
    users_df = pd.DataFrame(users_data)
    
    # Exibir usuários
    for _, user in users_df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 2])
            
            with col1:
                st.markdown(f"**{user['name']}**")
                st.caption(f"@{user['username']} | ID: {user['id']}")
            
            with col2:
                st.write(f"Tipo: {user['type'].replace('_', ' ').title()}")
                st.caption(f"Último login: {user['last_login']}")
            
            with col3:
                status_color = "🟢" if user['status'] == 'Ativo' else "🔴"
                st.markdown(f"{status_color} {user['status']}")
            
            with col4:
                if st.button("✏️", key=f"edit_user_{user['id']}", help="Editar"):
                    st.info("Funcionalidade de edição em desenvolvimento")
            
            with col5:
                col_suspend, col_delete = st.columns(2)
                
                with col_suspend:
                    if st.button("⏸️", key=f"suspend_user_{user['id']}", help="Suspender"):
                        st.warning("Usuário suspenso!")
                
                with col_delete:
                    if st.button("🗑️", key=f"delete_user_{user['id']}", help="Excluir"):
                        st.error("Usuário excluído!")
            
            st.divider()

def show_system_config():
    """Configurações do sistema"""
    st.markdown("### ⚙️ Configurações do Sistema")
    
    admin = AdminManager()
    config = admin.load_config()
    
    with st.form("system_config_form"):
        # Configurações gerais
        st.markdown("#### 🔧 Configurações Gerais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            system_name = st.text_input("Nome do Sistema", value=config.get("system_name", "NutriApp360"))
            max_users = st.number_input("Máximo de Usuários", min_value=1, max_value=1000, value=config.get("max_users", 100))
            session_timeout = st.number_input("Timeout de Sessão (min)", min_value=5, max_value=480, value=config.get("session_timeout", 30))
        
        with col2:
            backup_frequency = st.selectbox("Frequência de Backup", 
                                          ["hourly", "daily", "weekly"], 
                                          index=["hourly", "daily", "weekly"].index(config.get("backup_frequency", "daily")))
            
            email_notifications = st.checkbox("Notificações por E-mail", value=config.get("email_notifications", True))
            maintenance_mode = st.checkbox("Modo de Manutenção", value=config.get("maintenance_mode", False))
        
        # Recursos do sistema
        st.markdown("#### 🎯 Recursos do Sistema")
        
        features = config.get("features", {})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            patient_portal = st.checkbox("Portal do Paciente", value=features.get("patient_portal", True))
            mobile_app = st.checkbox("Aplicativo Móvel", value=features.get("mobile_app", True))
        
        with col2:
            reports = st.checkbox("Relatórios", value=features.get("reports", True))
            integrations = st.checkbox("Integrações", value=features.get("integrations", False))
        
        with col3:
            advanced_analytics = st.checkbox("Analytics Avançados", value=features.get("advanced_analytics", False))
        
        # Configurações de segurança
        st.markdown("#### 🔒 Configurações de Segurança")
        
        security = config.get("security", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            password_min_length = st.number_input("Tamanho Mínimo da Senha", 
                                                min_value=4, max_value=20, 
                                                value=security.get("password_min_length", 6))
            
            login_attempts = st.number_input("Tentativas de Login", 
                                           min_value=1, max_value=10, 
                                           value=security.get("login_attempts", 3))
        
        with col2:
            session_encryption = st.checkbox("Criptografia de Sessão", 
                                           value=security.get("session_encryption", True))
            
            two_factor_auth = st.checkbox("Autenticação de Dois Fatores", 
                                        value=security.get("two_factor_auth", False))
        
        # Botão para salvar
        if st.form_submit_button("💾 Salvar Configurações", use_container_width=True):
            new_config = {
                "system_name": system_name,
                "version": config.get("version", "1.0.0"),
                "max_users": max_users,
                "session_timeout": session_timeout,
                "backup_frequency": backup_frequency,
                "email_notifications": email_notifications,
                "maintenance_mode": maintenance_mode,
                "default_language": config.get("default_language", "pt-BR"),
                "theme": config.get("theme", "light"),
                "features": {
                    "patient_portal": patient_portal,
                    "mobile_app": mobile_app,
                    "reports": reports,
                    "integrations": integrations,
                    "advanced_analytics": advanced_analytics
                },
                "security": {
                    "password_min_length": password_min_length,
                    "session_encryption": session_encryption,
                    "two_factor_auth": two_factor_auth,
                    "login_attempts": login_attempts
                }
            }
            
            admin.save_config(new_config)
            st.success("✅ Configurações salvas com sucesso!")
            st.rerun()

def show_system_logs():
    """Logs do sistema"""
    st.markdown("### 📋 Logs do Sistema")
    
    # Filtros de log
    col1, col2, col3 = st.columns(3)
    
    with col1:
        log_level = st.selectbox("Nível", ["Todos", "Info", "Warning", "Error", "Critical"])
    
    with col2:
        date_range = st.date_input("Data", value=datetime.now().date())
    
    with col3:
        search_log = st.text_input("🔍 Buscar nos logs")
    
    # Logs simulados
    logs_data = [
        {"timestamp": "2024-09-04 09:30:15", "level": "Info", "user": "admin", "action": "Login realizado", "ip": "192.168.1.100"},
        {"timestamp": "2024-09-04 09:25:42", "level": "Info", "user": "dr.ana", "action": "Paciente criado: PAC_0045", "ip": "192.168.1.101"},
        {"timestamp": "2024-09-04 09:20:33", "level": "Warning", "user": "system", "action": "Backup demorou mais que o esperado", "ip": "localhost"},
        {"timestamp": "2024-09-04 09:15:21", "level": "Info", "user": "maria.silva", "action": "Diário alimentar atualizado", "ip": "192.168.1.102"},
        {"timestamp": "2024-09-04 09:10:18", "level": "Error", "user": "system", "action": "Falha ao enviar e-mail de notificação", "ip": "localhost"},
        {"timestamp": "2024-09-04 09:05:45", "level": "Info", "user": "nutri.carlos", "action": "Plano alimentar criado", "ip": "192.168.1.103"}
    ]
    
    # Exibir logs
    for log in logs_data:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 4])
            
            with col1:
                st.write(log["timestamp"])
            
            with col2:
                level_colors = {
                    "Info": "🔵",
                    "Warning": "🟡", 
                    "Error": "🔴",
                    "Critical": "🟣"
                }
                st.write(f"{level_colors.get(log['level'], '⚪')} {log['level']}")
            
            with col3:
                st.write(log["user"])
            
            with col4:
                st.write(f"{log['action']} | IP: {log['ip']}")
            
            st.divider()

def show_backup_restore():
    """Backup e restauração"""
    st.markdown("### 💾 Backup e Restauração")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📦 Criar Backup")
        
        backup_options = st.multiselect(
            "Selecionar dados para backup:",
            ["Usuários", "Pacientes", "Planos Alimentares", "Consultas", "Configurações", "Logs"],
            default=["Usuários", "Pacientes", "Planos Alimentares", "Configurações"]
        )
        
        backup_name = st.text_input("Nome do backup", value=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        include_media = st.checkbox("Incluir arquivos de mídia")
        compress_backup = st.checkbox("Comprimir backup", value=True)
        
        if st.button("🚀 Criar Backup", use_container_width=True):
            with st.spinner("Criando backup..."):
                # Simular criação de backup
                import time
                time.sleep(2)
                st.success(f"✅ Backup '{backup_name}' criado com sucesso!")
    
    with col2:
        st.markdown("#### 📥 Restaurar Backup")
        
        # Lista de backups disponíveis (simulada)
        available_backups = [
            {"name": "backup_20240904_030000", "date": "2024-09-04 03:00:00", "size": "25 MB"},
            {"name": "backup_20240903_030000", "date": "2024-09-03 03:00:00", "size": "24 MB"},
            {"name": "backup_20240902_030000", "date": "2024-09-02 03:00:00", "size": "23 MB"},
            {"name": "manual_backup_20240901", "date": "2024-09-01 15:30:00", "size": "22 MB"}
        ]
        
        backup_to_restore = st.selectbox(
            "Selecionar backup:",
            options=[b["name"] for b in available_backups],
            format_func=lambda x: f"{x} | {next(b['date'] for b in available_backups if b['name'] == x)}"
        )
        
        restore_options = st.multiselect(
            "Selecionar dados para restaurar:",
            ["Usuários", "Pacientes", "Planos Alimentares", "Consultas", "Configurações"],
            default=[]
        )
        
        if st.button("⚠️ Restaurar Backup", use_container_width=True, type="secondary"):
            if restore_options:
                st.warning("⚠️ Esta ação irá sobrescrever os dados atuais. Confirme para continuar.")
                
                col_cancel, col_confirm = st.columns(2)
                
                with col_cancel:
                    if st.button("❌ Cancelar"):
                        st.info("Operação cancelada.")
                
                with col_confirm:
                    if st.button("✅ Confirmar Restauração"):
                        with st.spinner("Restaurando backup..."):
                            import time
                            time.sleep(3)
                            st.success("✅ Backup restaurado com sucesso!")
            else:
                st.error("Selecione pelo menos um tipo de dado para restaurar.")
    
    # Configurações de backup automático
    st.markdown("---")
    st.markdown("#### ⚙️ Configurações de Backup Automático")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        auto_backup = st.checkbox("Backup Automático Ativo", value=True)
        backup_frequency = st.selectbox("Frequência", ["Diário", "Semanal", "Mensal"], index=0)
    
    with col2:
        backup_time = st.time_input("Horário do backup", value=datetime.strptime("03:00", "%H:%M").time())
        retention_days = st.number_input("Manter backups por (dias)", min_value=7, max_value=365, value=30)
    
    with col3:
        backup_location = st.selectbox("Local do backup", ["Local", "Nuvem", "Ambos"])
        email_on_backup = st.checkbox("Notificar por e-mail", value=True)
    
    if st.button("💾 Salvar Configurações de Backup", use_container_width=True):
        st.success("Configurações de backup atualizadas!")

def show_admin_dashboard():
    """Dashboard principal do administrador"""
    st.markdown("""
    <div style='background: linear-gradient(90deg, #FF6B6B, #FF8E8E); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>🔧 Painel de Administração</h1>
        <p style='color: white; margin: 0; opacity: 0.9;'>Gerencie o sistema e monitore operações</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs de administração
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Visão Geral", 
        "👥 Usuários", 
        "⚙️ Configurações", 
        "📋 Logs", 
        "💾 Backup"
    ])
    
    with tab1:
        show_system_overview()
    
    with tab2:
        show_user_management()
    
    with tab3:
        show_system_config()
    
    with tab4:
        show_system_logs()
    
    with tab5:
        show_backup_restore()

if __name__ == "__main__":
    show_admin_dashboard()