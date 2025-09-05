# modules/meal_plans.py
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import plotly.express as px

class MealPlanManager:
    def __init__(self):
        self.plans_file = 'data/meal_plans.json'
        self.foods_file = 'data/foods_database.json'
        self.recipes_file = 'data/recipes.json'
        self.ensure_data_directory()
        self.init_food_database()
    
    def ensure_data_directory(self):
        """Garante que o diretório de dados existe"""
        os.makedirs('data', exist_ok=True)
    
    def init_food_database(self):
        """Inicializa banco de dados de alimentos se não existir"""
        if not os.path.exists(self.foods_file):
            foods_db = {
                "cereais": {
                    "arroz_branco": {"nome": "Arroz branco cozido", "calorias": 128, "carboidratos": 28, "proteinas": 2.7, "gorduras": 0.3, "fibras": 0.4},
                    "arroz_integral": {"nome": "Arroz integral cozido", "calorias": 111, "carboidratos": 23, "proteinas": 2.6, "gorduras": 0.9, "fibras": 1.8},
                    "aveia": {"nome": "Aveia em flocos", "calorias": 389, "carboidratos": 66.3, "proteinas": 16.9, "gorduras": 6.9, "fibras": 10.6},
                    "quinoa": {"nome": "Quinoa cozida", "calorias": 120, "carboidratos": 22, "proteinas": 4.4, "gorduras": 1.9, "fibras": 2.8}
                },
                "proteinas": {
                    "frango_peito": {"nome": "Peito de frango grelhado", "calorias": 165, "carboidratos": 0, "proteinas": 31, "gorduras": 3.6, "fibras": 0},
                    "ovo": {"nome": "Ovo cozido", "calorias": 155, "carboidratos": 1.1, "proteinas": 13, "gorduras": 11, "fibras": 0},
                    "salmao": {"nome": "Salmão grelhado", "calorias": 208, "carboidratos": 0, "proteinas": 28, "gorduras": 10, "fibras": 0},
                    "tofu": {"nome": "Tofu", "calorias": 76, "carboidratos": 1.9, "proteinas": 8, "gorduras": 4.8, "fibras": 0.3}
                },
                "vegetais": {
                    "brocolis": {"nome": "Brócolis cozido", "calorias": 28, "carboidratos": 5.6, "proteinas": 3, "gorduras": 0.4, "fibras": 3.8},
                    "cenoura": {"nome": "Cenoura crua", "calorias": 41, "carboidratos": 9.6, "proteinas": 0.9, "gorduras": 0.2, "fibras": 2.8},
                    "espinafre": {"nome": "Espinafre cru", "calorias": 23, "carboidratos": 3.6, "proteinas": 2.9, "gorduras": 0.4, "fibras": 2.2},
                    "tomate": {"nome": "Tomate", "calorias": 18, "carboidratos": 3.9, "proteinas": 0.9, "gorduras": 0.2, "fibras": 1.2}
                },
                "frutas": {
                    "banana": {"nome": "Banana", "calorias": 89, "carboidratos": 23, "proteinas": 1.1, "gorduras": 0.3, "fibras": 2.6},
                    "maca": {"nome": "Maçã", "calorias": 52, "carboidratos": 14, "proteinas": 0.3, "gorduras": 0.2, "fibras": 2.4},
                    "laranja": {"nome": "Laranja", "calorias": 47, "carboidratos": 12, "proteinas": 0.9, "gorduras": 0.1, "fibras": 2.4},
                    "abacate": {"nome": "Abacate", "calorias": 160, "carboidratos": 8.5, "proteinas": 2, "gorduras": 14.7, "fibras": 6.7}
                }
            }
            
            with open(self.foods_file, 'w', encoding='utf-8') as f:
                json.dump(foods_db, f, indent=2, ensure_ascii=False)
    
    @st.cache_data
    def load_foods_database(_self):
        """Carrega banco de dados de alimentos"""
        with open(_self.foods_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @st.cache_data
    def load_meal_plans(_self):
        """Carrega planos alimentares"""
        if os.path.exists(_self.plans_file):
            with open(_self.plans_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_meal_plan(self, plan_data):
        """Salva plano alimentar"""
        plans = self.load_meal_plans()
        plan_id = f"PLAN_{len(plans) + 1:04d}"
        plan_data['id'] = plan_id
        plan_data['created_at'] = datetime.now().isoformat()
        plans[plan_id] = plan_data
        
        with open(self.plans_file, 'w', encoding='utf-8') as f:
            json.dump(plans, f, indent=2, ensure_ascii=False, default=str)
        
        return plan_id

def calculate_nutrition(foods_selected):
    """Calcula valores nutricionais totais"""
    total_calories = 0
    total_carbs = 0
    total_proteins = 0
    total_fats = 0
    total_fiber = 0
    
    for food_item in foods_selected:
        quantity = food_item.get('quantity', 0) / 100  # converter para porção de 100g
        food_data = food_item.get('nutrition', {})
        
        total_calories += food_data.get('calorias', 0) * quantity
        total_carbs += food_data.get('carboidratos', 0) * quantity
        total_proteins += food_data.get('proteinas', 0) * quantity
        total_fats += food_data.get('gorduras', 0) * quantity
        total_fiber += food_data.get('fibras', 0) * quantity
    
    return {
        'calorias': round(total_calories, 1),
        'carboidratos': round(total_carbs, 1),
        'proteinas': round(total_proteins, 1),
        'gorduras': round(total_fats, 1),
        'fibras': round(total_fiber, 1)
    }

def show_nutrition_chart(nutrition_data):
    """Exibe gráfico de macronutrientes"""
    macros = ['Carboidratos', 'Proteínas', 'Gorduras']
    values = [nutrition_data['carboidratos'], nutrition_data['proteinas'], nutrition_data['gorduras']]
    colors = ['#FF9999', '#66B2FF', '#99FF99']
    
    fig = px.pie(
        values=values,
        names=macros,
        color_discrete_sequence=colors,
        title="Distribuição de Macronutrientes"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_meal_plan_form():
    """Formulário para criar plano alimentar"""
    st.markdown("### 🍽️ Criar Novo Plano Alimentar")
    
    manager = MealPlanManager()
    foods_db = manager.load_foods_database()
    
    with st.form("meal_plan_form"):
        # Informações básicas do plano
        col1, col2 = st.columns(2)
        
        with col1:
            plan_name = st.text_input("Nome do Plano *")
            patient_id = st.text_input("ID do Paciente *")
            target_calories = st.number_input("Meta de Calorias Diárias", min_value=800, max_value=4000, value=2000)
        
        with col2:
            plan_duration = st.selectbox("Duração do Plano", ["1 semana", "2 semanas", "1 mês", "2 meses", "3 meses"])
            plan_type = st.selectbox("Tipo de Plano", ["Perda de peso", "Ganho de peso", "Manutenção", "Ganho de massa"])
            observations = st.text_area("Observações")
        
        st.markdown("#### 🍳 Refeições do Dia")
        
        # Estrutura para diferentes refeições
        meals = ["Café da manhã", "Lanche da manhã", "Almoço", "Lanche da tarde", "Jantar", "Ceia"]
        meal_plans = {}
        
        for meal in meals:
            with st.expander(f"🍽️ {meal}"):
                st.markdown(f"##### {meal}")
                
                # Seleção de alimentos por categoria
                meal_foods = []
                
                for category, foods in foods_db.items():
                    st.markdown(f"**{category.title()}:**")
                    
                    selected_foods = st.multiselect(
                        f"Selecionar {category}",
                        options=list(foods.keys()),
                        format_func=lambda x: foods[x]['nome'],
                        key=f"{meal}_{category}"
                    )
                    
                    for food_key in selected_foods:
                        food_data = foods[food_key]
                        
                        col_food, col_qty = st.columns([3, 1])
                        
                        with col_food:
                            st.write(f"• {food_data['nome']}")
                        
                        with col_qty:
                            quantity = st.number_input(
                                "Quantidade (g)",
                                min_value=0,
                                max_value=1000,
                                value=100,
                                step=10,
                                key=f"{meal}_{food_key}_qty"
                            )
                        
                        meal_foods.append({
                            'name': food_data['nome'],
                            'key': food_key,
                            'quantity': quantity,
                            'nutrition': food_data
                        })
                
                # Calcular nutrição da refeição
                if meal_foods:
                    meal_nutrition = calculate_nutrition(meal_foods)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Calorias", f"{meal_nutrition['calorias']}")
                    with col2:
                        st.metric("Carboidratos (g)", f"{meal_nutrition['carboidratos']}")
                    with col3:
                        st.metric("Proteínas (g)", f"{meal_nutrition['proteinas']}")
                    with col4:
                        st.metric("Gorduras (g)", f"{meal_nutrition['gorduras']}")
                
                meal_plans[meal] = {
                    'foods': meal_foods,
                    'nutrition': meal_nutrition if meal_foods else {}
                }
        
        # Botões do formulário
        col_cancel, col_preview, col_save = st.columns(3)
        
        with col_cancel:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.session_state.show_meal_plan_form = False
                st.rerun()
        
        with col_preview:
            preview_button = st.form_submit_button("👁️ Visualizar", use_container_width=True)
        
        with col_save:
            save_button = st.form_submit_button("💾 Salvar Plano", use_container_width=True, type="primary")
        
        if preview_button:
            # Mostrar prévia do plano
            st.markdown("### 📋 Prévia do Plano Alimentar")
            
            total_nutrition = {'calorias': 0, 'carboidratos': 0, 'proteinas': 0, 'gorduras': 0, 'fibras': 0}
            
            for meal, meal_data in meal_plans.items():
                if meal_data['foods']:
                    st.markdown(f"#### {meal}")
                    
                    for food in meal_data['foods']:
                        st.write(f"• {food['name']} - {food['quantity']}g")
                    
                    # Somar nutrição total
                    meal_nutrition = meal_data.get('nutrition', {})
                    for key in total_nutrition:
                        total_nutrition[key] += meal_nutrition.get(key, 0)
            
            # Mostrar resumo nutricional
            st.markdown("#### 📊 Resumo Nutricional Diário")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Calorias Totais", f"{total_nutrition['calorias']:.0f}")
            with col2:
                st.metric("Carboidratos (g)", f"{total_nutrition['carboidratos']:.1f}")
            with col3:
                st.metric("Proteínas (g)", f"{total_nutrition['proteinas']:.1f}")
            with col4:
                st.metric("Gorduras (g)", f"{total_nutrition['gorduras']:.1f}")
            with col5:
                st.metric("Fibras (g)", f"{total_nutrition['fibras']:.1f}")
            
            # Gráfico de macronutrientes
            show_nutrition_chart(total_nutrition)
        
        if save_button:
            if not plan_name or not patient_id:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                # Calcular nutrição total
                total_nutrition = {'calorias': 0, 'carboidratos': 0, 'proteinas': 0, 'gorduras': 0, 'fibras': 0}
                
                for meal_data in meal_plans.values():
                    meal_nutrition = meal_data.get('nutrition', {})
                    for key in total_nutrition:
                        total_nutrition[key] += meal_nutrition.get(key, 0)
                
                # Preparar dados do plano
                plan_data = {
                    'name': plan_name,
                    'patient_id': patient_id,
                    'target_calories': target_calories,
                    'duration': plan_duration,
                    'type': plan_type,
                    'observations': observations,
                    'meals': meal_plans,
                    'total_nutrition': total_nutrition,
                    'status': 'ativo'
                }
                
                # Salvar plano
                plan_id = manager.save_meal_plan(plan_data)
                st.success(f"✅ Plano alimentar salvo com sucesso! ID: {plan_id}")
                st.session_state.show_meal_plan_form = False
                st.rerun()

def show_meal_plans_list():
    """Exibe lista de planos alimentares"""
    manager = MealPlanManager()
    plans = manager.load_meal_plans()
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_patient = st.text_input("🔍 Buscar por paciente")
    
    with col2:
        filter_type = st.selectbox(
            "Filtrar por tipo",
            ['Todos', 'Perda de peso', 'Ganho de peso', 'Manutenção', 'Ganho de massa']
        )
    
    with col3:
        filter_status = st.selectbox("Status", ['Todos', 'ativo', 'inativo'])
    
    with col4:
        if st.button("➕ Novo Plano", use_container_width=True):
            st.session_state.show_meal_plan_form = True
            st.rerun()
    
    # Exibir planos
    if plans:
        st.markdown(f"### 🍽️ Planos Alimentares ({len(plans)} total)")
        
        for plan_id, plan_data in plans.items():
            # Aplicar filtros
            if search_patient and search_patient.lower() not in plan_data.get('patient_id', '').lower():
                continue
            
            if filter_type != 'Todos' and plan_data.get('type') != filter_type:
                continue
            
            if filter_status != 'Todos' and plan_data.get('status', 'ativo') != filter_status:
                continue
            
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 2])
                
                with col1:
                    st.markdown(f"**{plan_data.get('name', 'Plano sem nome')}**")
                    st.caption(f"Paciente: {plan_data.get('patient_id', 'N/A')} | Tipo: {plan_data.get('type', 'N/A')}")
                
                with col2:
                    total_cals = plan_data.get('total_nutrition', {}).get('calorias', 0)
                    st.metric("Calorias/dia", f"{total_cals:.0f}")
                
                with col3:
                    status_color = "🟢" if plan_data.get('status') == 'ativo' else "🔴"
                    st.markdown(f"{status_color} {plan_data.get('status', 'ativo').title()}")
                
                with col4:
                    col_view, col_edit = st.columns(2)
                    
                    with col_view:
                        if st.button("👁️", key=f"view_plan_{plan_id}", help="Visualizar"):
                            st.session_state.view_plan = plan_id
                            st.rerun()
                    
                    with col_edit:
                        if st.button("📧", key=f"send_plan_{plan_id}", help="Enviar para paciente"):
                            st.success("Plano enviado para o paciente!")
                
                st.divider()
    else:
        st.info("Nenhum plano alimentar cadastrado ainda.")

def show_plan_detail(plan_id):
    """Exibe detalhes de um plano alimentar"""
    manager = MealPlanManager()
    plans = manager.load_meal_plans()
    plan = plans.get(plan_id)
    
    if not plan:
        st.error("Plano não encontrado!")
        return
    
    # Header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"# 🍽️ {plan.get('name', 'Plano Alimentar')}")
        st.markdown(f"**Paciente:** {plan.get('patient_id')} | **Tipo:** {plan.get('type')} | **Duração:** {plan.get('duration')}")
    
    with col2:
        if st.button("🔙 Voltar", use_container_width=True):
            st.session_state.view_plan = None
            st.rerun()
        
        if st.button("📧 Enviar", use_container_width=True):
            st.success("Plano enviado para o paciente!")
    
    # Resumo nutricional
    total_nutrition = plan.get('total_nutrition', {})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Calorias", f"{total_nutrition.get('calorias', 0):.0f}")
    with col2:
        st.metric("Carboidratos", f"{total_nutrition.get('carboidratos', 0):.1f}g")
    with col3:
        st.metric("Proteínas", f"{total_nutrition.get('proteinas', 0):.1f}g")
    with col4:
        st.metric("Gorduras", f"{total_nutrition.get('gorduras', 0):.1f}g")
    with col5:
        st.metric("Fibras", f"{total_nutrition.get('fibras', 0):.1f}g")
    
    # Gráfico de macronutrientes
    col1, col2 = st.columns(2)
    
    with col1:
        show_nutrition_chart(total_nutrition)
    
    with col2:
        st.markdown("#### 📋 Informações do Plano")
        st.write(f"**Meta de Calorias:** {plan.get('target_calories', 0)} kcal")
        st.write(f"**Duração:** {plan.get('duration', 'N/A')}")
        st.write(f"**Status:** {plan.get('status', 'ativo').title()}")
        st.write(f"**Criado em:** {plan.get('created_at', 'N/A')[:10]}")
        
        if plan.get('observations'):
            st.markdown("**Observações:**")
            st.write(plan.get('observations'))
    
    # Detalhes das refeições
    st.markdown("---")
    st.markdown("### 🍽️ Refeições Detalhadas")
    
    meals = plan.get('meals', {})
    
    for meal_name, meal_data in meals.items():
        if meal_data.get('foods'):
            with st.expander(f"{meal_name} - {meal_data.get('nutrition', {}).get('calorias', 0):.0f} kcal"):
                
                # Lista de alimentos
                for food in meal_data['foods']:
                    col1, col2, col3 = st.columns([3, 1, 2])
                    
                    with col1:
                        st.write(f"• {food['name']}")
                    
                    with col2:
                        st.write(f"{food['quantity']}g")
                    
                    with col3:
                        food_cals = (food['nutrition'].get('calorias', 0) * food['quantity']) / 100
                        st.write(f"{food_cals:.0f} kcal")
                
                # Resumo nutricional da refeição
                meal_nutrition = meal_data.get('nutrition', {})
                
                st.markdown("**Resumo da refeição:**")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Calorias", f"{meal_nutrition.get('calorias', 0):.0f}")
                with col2:
                    st.metric("Carboidratos", f"{meal_nutrition.get('carboidratos', 0):.1f}g")
                with col3:
                    st.metric("Proteínas", f"{meal_nutrition.get('proteinas', 0):.1f}g")
                with col4:
                    st.metric("Gorduras", f"{meal_nutrition.get('gorduras', 0):.1f}g")

def show_meal_plans():
    """Função principal do módulo de planos alimentares"""
    # Verificar estado da sessão
    if st.session_state.get('show_meal_plan_form', False):
        show_meal_plan_form()
    elif st.session_state.get('view_plan'):
        show_plan_detail(st.session_state.view_plan)
    else:
        st.markdown("""
        <div style='background: linear-gradient(90deg, #4CAF50, #45a049); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; margin: 0;'>🍽️ Planos Alimentares</h1>
            <p style='color: white; margin: 0; opacity: 0.9;'>Crie e gerencie planos alimentares personalizados</p>
        </div>
        """, unsafe_allow_html=True)
        
        show_meal_plans_list()

# Inicializar estados da sessão
if 'show_meal_plan_form' not in st.session_state:
    st.session_state.show_meal_plan_form = False
if 'view_plan' not in st.session_state:
    st.session_state.view_plan = None

if __name__ == "__main__":
    show_meal_plans()