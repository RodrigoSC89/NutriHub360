# modules/patient_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import json
import os

class PatientDashboardManager:
    def __init__(self):
        self.food_diary_file = 'data/food_diary.json'
        self.patient_progress_file = 'data/patient_progress.json'
        self.appointments_file = 'data/appointments.json'
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Garante que o diretório de dados existe"""
        os.makedirs('data', exist_ok=True)
    
    @st.cache_data
    def load_food_diary(_self, patient_id):
        """Carrega diário alimentar do paciente"""
        if os.path.exists(_self.food_diary_file):
            with open(_self.food_diary_file, 'r', encoding='utf-8') as f:
                all_diaries = json.load(f)
                return all_diaries.get(patient_id, {})
        return {}
    
    @st.cache_data
    def load_patient_progress(_self, patient_id):
        """Carrega progresso do paciente"""
        if os.path.exists(_self.patient_progress_file):
            with open(_self.patient_progress_file, 'r', encoding='utf-8') as f:
                all_progress = json.load(f)
                return all_progress.get(patient_id, {})
        return {}
    
    def save_food_entry(self, patient_id, date_str, meal_type, food_data):
        """Salva entrada no diário alimentar"""
        # Carregar dados existentes
        all_diaries = {}
        if os.path.exists(self.food_diary_file):
            with open(self.food_diary_file, 'r', encoding='utf-8') as f:
                all_diaries = json.load(f)
        
        # Inicializar estrutura se necessário
        if patient_id not in all_diaries:
            all_diaries[patient_id] = {}
        if date_str not in all_diaries[patient_id]:
            all_diaries[patient_id][date_str] = {}
        if meal_type not in all_diaries[patient_id][date_str]:
            all_diaries[patient_id][date_str][meal_type] = []
        
        # Adicionar nova entrada
        all_diaries[patient_id][date_str][meal_type].append({
            **food_data,
            'timestamp': datetime.now().isoformat()
        })
        
        # Salvar
        with open(self.food_diary_file, 'w', encoding='utf-8') as f:
            json.dump(all_diaries, f, indent=2, ensure_ascii=False, default=str)
    
    def save_progress_entry(self, patient_id, progress_data):
        """Salva entrada de progresso"""
        # Carregar dados existentes
        all_progress = {}
        if os.path.exists(self.patient_progress_file):
            with open(self.patient_progress_file, 'r', encoding='utf-8') as f:
                all_progress = json.load(f)
        
        # Inicializar se necessário
        if patient_id not in all_progress:
            all_progress[patient_id] = []
        
        # Adicionar nova entrada
        progress_data['timestamp'] = datetime.now().isoformat()
        all_progress[patient_id].append(progress_data)
        
        # Salvar
        with open(self.patient_progress_file, 'w', encoding='utf-8') as f:
            json.dump(all_progress, f, indent=2, ensure_ascii=False, default=str)

def get_patient_data():
    """Simula dados do paciente logado"""
    return {
        'id': 'PAC_0001',
        'nome': 'Maria Silva',
        'objetivo': 'Perda de peso',
        'peso_inicial': 75.0,
        'peso_meta': 65.0,
        'altura': 1.65,
        'imc_inicial': 27.5,
        'data_inicio': '2024-01-15'
    }

def show_patient_metrics():
    """Exibe métricas principais do paciente"""
    patient_data = get_patient_data()
    
    # Simular dados de progresso
    current_weight = 71.2
    weight_lost = patient_data['peso_inicial'] - current_weight
    weight_to_goal = current_weight - patient_data['peso_meta']
    current_bmi = current_weight / (patient_data['altura'] ** 2)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Peso Atual",
            f"{current_weight} kg",
            f"-{weight_lost:.1f} kg"
        )
    
    with col2:
        st.metric(
            "IMC Atual",
            f"{current_bmi:.1f}",
            f"-{patient_data['imc_inicial'] - current_bmi:.1f}"
        )
    
    with col3:
        progress_percent = (weight_lost / (patient_data['peso_inicial'] - patient_data['peso_meta'])) * 100
        st.metric(
            "Progresso",
            f"{progress_percent:.1f}%",
            "da meta"
        )
    
    with col4:
        st.metric(
            "Meta Restante",
            f"{weight_to_goal:.1f} kg",
            "para objetivo"
        )
    
    with col5:
        days_in_program = (datetime.now() - datetime.fromisoformat(patient_data['data_inicio'])).days
        st.metric(
            "Dias no Programa",
            f"{days_in_program}",
            "dias"
        )

def show_weight_progress_chart():
    """Exibe gráfico de evolução de peso"""
    # Dados simulados de evolução
    dates = pd.date_range(start='2024-01-15', end=datetime.now().date(), freq='W')
    weights = [75.0, 74.5, 74.0, 73.2, 72.8, 72.1, 71.8, 71.2][:len(dates)]
    
    progress_df = pd.DataFrame({
        'Data': dates,
        'Peso': weights
    })
    
    fig = px.line(
        progress_df,
        x='Data',
        y='Peso',
        title='📈 Evolução do Peso',
        color_discrete_sequence=['#4CAF50']
    )
    
    # Adicionar linha da meta
    fig.add_hline(y=65.0, line_dash="dash", line_color="red", 
                  annotation_text="Meta: 65kg", annotation_position="bottom right")
    
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Peso (kg)",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_todays_plan():
    """Exibe plano alimentar do dia"""
    st.markdown("### 🍽️ Seu Plano de Hoje")
    
    # Dados simulados do plano
    todays_meals = {
        "Café da manhã": {
            "foods": ["Aveia com frutas", "Leite desnatado", "1 banana"],
            "calories": 320,
            "completed": True
        },
        "Lanche da manhã": {
            "foods": ["Iogurte natural", "1 maçã"],
            "calories": 150,
            "completed": True
        },
        "Almoço": {
            "foods": ["Peito de frango grelhado", "Arroz integral", "Salada verde", "Feijão"],
            "calories": 450,
            "completed": False
        },
        "Lanche da tarde": {
            "foods": ["Castanhas", "Chá verde"],
            "calories": 120,
            "completed": False
        },
        "Jantar": {
            "foods": ["Salmão grelhado", "Batata doce", "Brócolis"],
            "calories": 380,
            "completed": False
        }
    }
    
    total_calories = sum(meal['calories'] for meal in todays_meals.values())
    completed_calories = sum(meal['calories'] for meal in todays_meals.values() if meal['completed'])
    
    # Progresso do dia
    progress = (completed_calories / total_calories) * 100
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.progress(progress / 100)
        st.write(f"Progresso do dia: {progress:.0f}% ({completed_calories}/{total_calories} kcal)")
    
    with col2:
        remaining_calories = total_calories - completed_calories
        st.metric("Calorias Restantes", f"{remaining_calories} kcal")
    
    # Listar refeições
    for meal, data in todays_meals.items():
        with st.container():
            col_meal, col_cals, col_status, col_action = st.columns([3, 1, 1, 1])
            
            with col_meal:
                status_icon = "✅" if data['completed'] else "⏰"
                st.markdown(f"**{status_icon} {meal}**")
                st.caption(", ".join(data['foods']))
            
            with col_cals:
                st.metric("", f"{data['calories']} kcal")
            
            with col_status:
                if data['completed']:
                    st.success("Concluído")
                else:
                    st.info("Pendente")
            
            with col_action:
                if not data['completed']:
                    if st.button("✓", key=f"complete_{meal}", help="Marcar como consumido"):
                        st.success(f"{meal} marcada como consumida!")
                        # Aqui salvaria no banco de dados
            
            st.divider()

def show_food_diary_quick_add():
    """Formulário rápido para adicionar ao diário"""
    st.markdown("### 📝 Adicionar ao Diário Alimentar")
    
    with st.form("quick_food_entry"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            meal_type = st.selectbox(
                "Refeição",
                ["Café da manhã", "Lanche da manhã", "Almoço", "Lanche da tarde", "Jantar", "Ceia"]
            )
        
        with col2:
            food_item = st.text_input("Alimento")
        
        with col3:
            quantity = st.text_input("Quantidade", placeholder="ex: 100g, 1 unidade")
        
        observations = st.text_area("Observações (opcional)", placeholder="Como se sentiu, local, etc.")
        
        if st.form_submit_button("➕ Adicionar", use_container_width=True):
            if food_item:
                # Simular salvamento
                st.success(f"✅ {food_item} adicionado ao {meal_type}!")
            else:
                st.error("Por favor, informe o alimento.")

def show_next_appointment():
    """Exibe próxima consulta"""
    st.markdown("### 📅 Próxima Consulta")
    
    # Dados simulados
    next_appointment = {
        'date': '2024-09-10',
        'time': '14:30',
        'type': 'Consulta de retorno',
        'nutritionist': 'Dra. Ana Nutricionista',
        'location': 'Consultório - Sala 2'
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**📅 {next_appointment['date']} às {next_appointment['time']}**")
        st.write(f"**Tipo:** {next_appointment['type']}")
        st.write(f"**Nutricionista:** {next_appointment['nutritionist']}")
        st.write(f"**Local:** {next_appointment['location']}")
    
    with col2:
        if st.button("💬 Enviar Mensagem", use_container_width=True):
            st.session_state.current_page = 'chat'
            st.rerun()
        
        if st.button("📅 Reagendar", use_container_width=True):
            st.info("Funcionalidade de reagendamento em desenvolvimento")

def show_achievements_and_tips():
    """Exibe conquistas e dicas"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Suas Conquistas")
        
        achievements = [
            {"title": "Primeira semana completa", "icon": "🎯", "completed": True},
            {"title": "5kg perdidos", "icon": "⚖️", "completed": True},
            {"title": "30 dias consecutivos", "icon": "📅", "completed": False},
            {"title": "Meta de hidratação", "icon": "💧", "completed": True},
            {"title": "Exercício 3x/semana", "icon": "🏃‍♀️", "completed": False}
        ]
        
        for achievement in achievements:
            if achievement['completed']:
                st.success(f"{achievement['icon']} {achievement['title']}")
            else:
                st.info(f"{achievement['icon']} {achievement['title']} (em progresso)")
    
    with col2:
        st.markdown("### 💡 Dica do Dia")
        
        tips = [
            "Beba um copo de água antes de cada refeição para aumentar a saciedade.",
            "Mastigue devagar e saboreie cada garfada. Isso ajuda na digestão e satisfação.",
            "Inclua proteínas em todas as refeições para manter-se saciado por mais tempo.",
            "Prepare suas refeições com antecedência para evitar escolhas impulsivas.",
            "Durma pelo menos 7-8 horas por noite - o sono inadequado afeta os hormônios da fome."
        ]
        
        import random
        daily_tip = random.choice(tips)
        
        st.info(daily_tip)
        
        st.markdown("### 🔔 Lembretes")
        st.write("• Tomar suplemento de vitamina D")
        st.write("• Registrar peso de amanhã")
        st.write("• Beber 2L de água hoje")

def show_hydration_tracker():
    """Tracker de hidratação"""
    st.markdown("### 💧 Controle de Hidratação")
    
    target_water = 2000  # ml
    current_water = 1200  # ml simulado
    
    progress = (current_water / target_water) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Meta Diária", f"{target_water} ml")
    
    with col2:
        st.metric("Consumido", f"{current_water} ml")
    
    with col3:
        remaining = target_water - current_water
        st.metric("Restante", f"{remaining} ml")
    
    # Barra de progresso
    st.progress(min(progress / 100, 1.0))
    st.write(f"Progresso: {progress:.0f}%")
    
    # Botões rápidos para adicionar água
    st.markdown("#### Adicionar:")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Copo 200ml", use_container_width=True):
            st.success("200ml adicionados!")
    
    with col2:
        if st.button("Garrafa 500ml", use_container_width=True):
            st.success("500ml adicionados!")
    
    with col3:
        if st.button("Garrafa 1L", use_container_width=True):
            st.success("1000ml adicionados!")
    
    with col4:
        custom_amount = st.number_input("Personalizado (ml)", min_value=0, max_value=1000, step=50, key="custom_water")
        if st.button("Adicionar", use_container_width=True):
            if custom_amount > 0:
                st.success(f"{custom_amount}ml adicionados!")

def show_mood_and_energy():
    """Registro de humor e energia"""
    st.markdown("### 😊 Como você está se sentindo hoje?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Energia")
        energy_level = st.slider("Nível de energia", 1, 10, 7, key="energy")
        
        energy_emoji = {
            1: "😴", 2: "😴", 3: "😪", 4: "😐", 5: "😐", 
            6: "🙂", 7: "😊", 8: "😃", 9: "🤗", 10: "⚡"
        }
        
        st.markdown(f"### {energy_emoji[energy_level]}")
    
    with col2:
        st.markdown("#### Humor")
        mood_level = st.slider("Humor geral", 1, 10, 8, key="mood")
        
        mood_emoji = {
            1: "😢", 2: "😞", 3: "😕", 4: "😐", 5: "😐",
            6: "🙂", 7: "😊", 8: "😃", 9: "😄", 10: "🥳"
        }
        
        st.markdown(f"### {mood_emoji[mood_level]}")
    
    # Fatores que influenciaram
    st.markdown("#### O que influenciou seu dia?")
    factors = st.multiselect(
        "Selecione os fatores:",
        ["Boa alimentação", "Exercício", "Sono adequado", "Estresse", "Trabalho", "Família", "Clima", "Outros"]
    )
    
    notes = st.text_area("Observações adicionais")
    
    if st.button("💾 Salvar registro do dia", use_container_width=True):
        st.success("Registro salvo! Obrigado por compartilhar como se sente.")

def show_patient_dashboard():
    """Função principal do dashboard do paciente"""
    patient_data = get_patient_data()
    
    # Header personalizado
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #4CAF50, #45a049); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>🏠 Olá, {patient_data['nome']}!</h1>
        <p style='color: white; margin: 0; opacity: 0.9;'>Acompanhe seu progresso e mantenha-se motivado</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principais
    show_patient_metrics()
    
    st.divider()
    
    # Layout em colunas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de evolução
        show_weight_progress_chart()
        
        st.markdown("---")
        
        # Plano do dia
        show_todays_plan()
    
    with col2:
        # Próxima consulta
        show_next_appointment()
        
        st.markdown("---")
        
        # Adicionar alimento rapidamente
        show_food_diary_quick_add()
        
        st.markdown("---")
        
        # Controle de hidratação
        show_hydration_tracker()
    
    # Seção em largura total
    st.markdown("---")
    
    # Conquistas e dicas
    show_achievements_and_tips()
    
    st.markdown("---")
    
    # Humor e energia
    show_mood_and_energy()
    
    # Rodapé com motivação
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background-color: #f0f8f0; border-radius: 10px;'>
        <h3 style='color: #4CAF50; margin: 0;'>💪 Continue assim!</h3>
        <p style='margin: 0;'>Cada dia é uma nova oportunidade para cuidar de você mesmo.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_patient_dashboard()