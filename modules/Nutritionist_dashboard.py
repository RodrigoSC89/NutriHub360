# modules/nutritionist_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

@st.cache_data
def load_dashboard_data():
    """Carrega dados para o dashboard"""
    # Dados simulados - em produção viriam de banco de dados
    patients_data = {
        'total_patients': 45,
        'active_patients': 38,
        'new_this_month': 8,
        'appointments_today': 6,
        'upcoming_appointments': 12
    }
    
    # Dados de evolução dos pacientes
    evolution_data = pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', end='2024-12-31', freq='M'),
        'weight_loss': [2.5, 3.1, 2.8, 4.2, 3.5, 2.9, 3.8, 4.1, 3.2, 2.7, 3.6, 4.0],
        'adherence': [78, 82, 79, 85, 83, 80, 87, 89, 84, 81, 86, 88],
        'new_patients': [3, 5, 4, 7, 6, 4, 8, 6, 5, 4, 7, 8]
    })
    
    return patients_data, evolution_data

def show_key_metrics(patients_data):
    """Exibe métricas principais"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="👥 Total de Pacientes",
            value=patients_data['total_patients'],
            delta=f"+{patients_data['new_this_month']} este mês"
        )
    
    with col2:
        st.metric(
            label="✅ Pacientes Ativos",
            value=patients_data['active_patients'],
            delta="84% do total"
        )
    
    with col3:
        st.metric(
            label="📅 Consultas Hoje",
            value=patients_data['appointments_today'],
            delta="6 de 8 agendadas"
        )
    
    with col4:
        st.metric(
            label="⏰ Próximas Consultas",
            value=patients_data['upcoming_appointments'],
            delta="Esta semana"
        )
    
    with col5:
        st.metric(
            label="🎯 Taxa de Adesão",
            value="85%",
            delta="+3% vs mês anterior"
        )

def show_evolution_charts(evolution_data):
    """Exibe gráficos de evolução"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Evolução Média de Peso dos Pacientes")
        fig_weight = px.line(
            evolution_data, 
            x='date', 
            y='weight_loss',
            title='Perda de Peso Média (kg/mês)',
            color_discrete_sequence=['#4CAF50']
        )
        fig_weight.update_layout(
            xaxis_title="Período",
            yaxis_title="Perda de Peso (kg)",
            showlegend=False
        )
        st.plotly_chart(fig_weight, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Taxa de Adesão ao Tratamento")
        fig_adherence = px.bar(
            evolution_data, 
            x='date', 
            y='adherence',
            title='Adesão Mensal (%)',
            color='adherence',
            color_continuous_scale='Greens'
        )
        fig_adherence.update_layout(
            xaxis_title="Período",
            yaxis_title="Taxa de Adesão (%)",
            showlegend=False
        )
        st.plotly_chart(fig_adherence, use_container_width=True)

def show_recent_activities():
    """Exibe atividades recentes"""
    st.markdown("#### 🕒 Atividades Recentes")
    
    activities = [
        {"time": "10:30", "patient": "Maria Silva", "action": "Consulta realizada", "status": "✅"},
        {"time": "09:15", "patient": "João Santos", "action": "Plano alimentar atualizado", "status": "📝"},
        {"time": "08:45", "patient": "Ana Costa", "action": "Mensagem recebida", "status": "💬"},
        {"time": "Ontem", "patient": "Carlos Lima", "action": "Meta de peso atingida", "status": "🎯"},
        {"time": "Ontem", "patient": "Lucia Ferreira", "action": "Consulta agendada", "status": "📅"}
    ]
    
    for activity in activities:
        col1, col2, col3, col4 = st.columns([1, 3, 4, 1])
        with col1:
            st.text(activity["time"])
        with col2:
            st.text(activity["patient"])
        with col3:
            st.text(activity["action"])
        with col4:
            st.text(activity["status"])

def show_upcoming_appointments():
    """Exibe próximas consultas"""
    st.markdown("#### 📅 Próximas Consultas")
    
    appointments = pd.DataFrame({
        'Horário': ['14:00', '15:30', '16:00', '17:00'],
        'Paciente': ['Roberto Alves', 'Fernanda Lima', 'Pedro Costa', 'Julia Santos'],
        'Tipo': ['Retorno', 'Primeira consulta', 'Reavaliação', 'Acompanhamento'],
        'Status': ['Confirmado', 'Aguardando', 'Confirmado', 'Confirmado']
    })
    
    st.dataframe(
        appointments,
        use_container_width=True,
        hide_index=True
    )

def show_quick_actions():
    """Exibe ações rápidas"""
    st.markdown("#### ⚡ Ações Rápidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👤 Novo Paciente", use_container_width=True):
            st.session_state.current_page = 'new_patient'
            st.rerun()
    
    with col2:
        if st.button("🍽️ Criar Plano", use_container_width=True):
            st.session_state.current_page = 'create_meal_plan'
            st.rerun()
    
    with col3:
        if st.button("📝 Nova Consulta", use_container_width=True):
            st.session_state.current_page = 'new_appointment'
            st.rerun()
    
    with col4:
        if st.button("📊 Relatórios", use_container_width=True):
            st.session_state.current_page = 'reports'
            st.rerun()

def show_patient_alerts():
    """Exibe alertas importantes sobre pacientes"""
    st.markdown("#### ⚠️ Alertas Importantes")
    
    alerts = [
        {"type": "warning", "message": "3 pacientes não registraram alimentação há 2 dias"},
        {"type": "info", "message": "5 pacientes próximos da meta de peso"},
        {"type": "success", "message": "8 pacientes atingiram metas esta semana"},
        {"type": "error", "message": "1 paciente com baixa adesão ao tratamento"}
    ]
    
    for alert in alerts:
        if alert["type"] == "warning":
            st.warning(alert["message"])
        elif alert["type"] == "info":
            st.info(alert["message"])
        elif alert["type"] == "success":
            st.success(alert["message"])
        elif alert["type"] == "error":
            st.error(alert["message"])

def show_performance_summary():
    """Exibe resumo de performance do nutricionista"""
    st.markdown("#### 🎯 Seu Desempenho Este Mês")
    
    performance_data = {
        'Consultas Realizadas': 32,
        'Planos Criados': 15,
        'Metas Atingidas pelos Pacientes': 28,
        'Taxa de Satisfação': '4.8/5.0',
        'Receita Gerada': 'R$ 8.400'
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        for key, value in list(performance_data.items())[:3]:
            st.metric(label=key, value=value)
    
    with col2:
        for key, value in list(performance_data.items())[3:]:
            st.metric(label=key, value=value)

def show_nutritionist_dashboard():
    """Função principal do dashboard do nutricionista"""
    # Header personalizado
    st.markdown("""
    <div style='background: linear-gradient(90deg, #4CAF50, #45a049); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>🥗 Dashboard do Nutricionista</h1>
        <p style='color: white; margin: 0; opacity: 0.9;'>Gerencie seus pacientes e acompanhe resultados</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    patients_data, evolution_data = load_dashboard_data()
    
    # Métricas principais
    show_key_metrics(patients_data)
    
    st.divider()
    
    # Gráficos de evolução
    show_evolution_charts(evolution_data)
    
    st.divider()
    
    # Layout em duas colunas para seções diferentes
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Próximas consultas
        show_upcoming_appointments()
        
        st.markdown("---")
        
        # Atividades recentes
        show_recent_activities()
    
    with col2:
        # Ações rápidas
        show_quick_actions()
        
        st.markdown("---")
        
        # Alertas
        show_patient_alerts()
        
        st.markdown("---")
        
        # Performance
        show_performance_summary()
    
    # Seção de dicas e recursos
    st.markdown("---")
    
    with st.expander("💡 Dicas e Recursos"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **📚 Recursos Educacionais**
            - Biblioteca de artigos científicos
            - Webinars e cursos
            - Calculadoras nutricionais
            """)
        
        with col2:
            st.markdown("""
            **🔧 Ferramentas Úteis**
            - Templates de anamnese
            - Modelos de planos alimentares
            - Receitas saudáveis
            """)
        
        with col3:
            st.markdown("""
            **📞 Suporte**
            - Chat com suporte técnico
            - Central de ajuda
            - Comunidade de nutricionistas
            """)

if __name__ == "__main__":
    show_nutritionist_dashboard()