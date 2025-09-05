# modules/calculators.py
import streamlit as st
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def calculate_bmr(weight, height, age, sex):
    """Calcula Taxa Metabólica Basal usando equação de Harris-Benedict revisada"""
    if sex == "Masculino":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    return round(bmr, 1)

def calculate_tdee(bmr, activity_level):
    """Calcula Gasto Energético Total Diário"""
    activity_factors = {
        "Sedentário": 1.2,
        "Levemente ativo": 1.375,
        "Moderadamente ativo": 1.55,
        "Muito ativo": 1.725,
        "Extremamente ativo": 1.9
    }
    
    return round(bmr * activity_factors[activity_level], 1)

def calculate_bmi(weight, height):
    """Calcula Índice de Massa Corporal"""
    bmi = weight / (height ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Retorna categoria do IMC"""
    if bmi < 18.5:
        return "Abaixo do peso", "blue"
    elif bmi < 25:
        return "Peso normal", "green"
    elif bmi < 30:
        return "Sobrepeso", "orange"
    else:
        return "Obesidade", "red"

def calculate_ideal_weight(height, sex):
    """Calcula peso ideal usando diferentes fórmulas"""
    height_cm = height * 100
    
    # Fórmula de Robinson (1983)
    if sex == "Masculino":
        robinson = 52 + (1.9 * (height_cm - 152.4) / 2.54)
    else:
        robinson = 49 + (1.7 * (height_cm - 152.4) / 2.54)
    
    # Fórmula de Miller (1983)
    if sex == "Masculino":
        miller = 56.2 + (1.41 * (height_cm - 152.4) / 2.54)
    else:
        miller = 53.1 + (1.36 * (height_cm - 152.4) / 2.54)
    
    # Fórmula de Devine (1974)
    if sex == "Masculino":
        devine = 50 + (2.3 * (height_cm - 152.4) / 2.54)
    else:
        devine = 45.5 + (2.3 * (height_cm - 152.4) / 2.54)
    
    return {
        "Robinson": round(robinson, 1),
        "Miller": round(miller, 1),
        "Devine": round(devine, 1)
    }

def calculate_macros(calories, carb_percent, protein_percent, fat_percent):
    """Calcula distribuição de macronutrientes"""
    carb_calories = calories * (carb_percent / 100)
    protein_calories = calories * (protein_percent / 100)
    fat_calories = calories * (fat_percent / 100)
    
    carb_grams = carb_calories / 4  # 4 kcal/g
    protein_grams = protein_calories / 4  # 4 kcal/g
    fat_grams = fat_calories / 9  # 9 kcal/g
    
    return {
        "carboidratos": round(carb_grams, 1),
        "proteinas": round(protein_grams, 1),
        "gorduras": round(fat_grams, 1)
    }

def calculate_water_needs(weight, activity_level):
    """Calcula necessidade hídrica"""
    base_water = weight * 35  # 35ml por kg de peso
    
    activity_factors = {
        "Sedentário": 1.0,
        "Levemente ativo": 1.1,
        "Moderadamente ativo": 1.2,
        "Muito ativo": 1.3,
        "Extremamente ativo": 1.4
    }
    
    total_water = base_water * activity_factors[activity_level]
    return round(total_water, 0)

def show_bmr_calculator():
    """Calculadora de TMB e GET"""
    st.markdown("### 🔥 Calculadora de TMB e GET")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Peso (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1)
        height = st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
    
    with col2:
        age = st.number_input("Idade (anos)", min_value=10, max_value=120, value=30)
        sex = st.selectbox("Sexo", ["Masculino", "Feminino"])
    
    activity_level = st.selectbox(
        "Nível de Atividade Física",
        ["Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo", "Extremamente ativo"],
        help="Sedentário: Pouco ou nenhum exercício\nLevemente ativo: Exercício leve 1-3x/semana\nModeradamente ativo: Exercício moderado 3-5x/semana\nMuito ativo: Exercício intenso 6-7x/semana\nExtremamente ativo: Exercício muito intenso 2x/dia"
    )
    
    if st.button("Calcular TMB e GET", use_container_width=True):
        height_m = height / 100
        bmr = calculate_bmr(weight, height, age, sex)
        tdee = calculate_tdee(bmr, activity_level)
        
        # Resultados
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("TMB (Taxa Metabólica Basal)", f"{bmr} kcal/dia")
        
        with col2:
            st.metric("GET (Gasto Energético Total)", f"{tdee} kcal/dia")
        
        with col3:
            weight_maintenance = tdee
            st.metric("Para manter peso", f"{weight_maintenance:.0f} kcal/dia")
        
        # Recomendações para objetivos
        st.markdown("#### 🎯 Recomendações por Objetivo")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🔻 Perda de Peso**")
            deficit_500 = tdee - 500
            deficit_750 = tdee - 750
            st.write(f"Déficit moderado: {deficit_500:.0f} kcal/dia")
            st.write(f"Déficit agressivo: {deficit_750:.0f} kcal/dia")
        
        with col2:
            st.markdown("**📈 Ganho de Peso**")
            surplus_300 = tdee + 300
            surplus_500 = tdee + 500
            st.write(f"Ganho lento: {surplus_300:.0f} kcal/dia")
            st.write(f"Ganho rápido: {surplus_500:.0f} kcal/dia")
        
        with col3:
            st.markdown("**⚖️ Manutenção**")
            maintenance_min = tdee - 100
            maintenance_max = tdee + 100
            st.write(f"Faixa ideal: {maintenance_min:.0f} - {maintenance_max:.0f} kcal/dia")

def show_bmi_calculator():
    """Calculadora de IMC"""
    st.markdown("### 📏 Calculadora de IMC")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        weight = st.number_input("Peso (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1, key="bmi_weight")
    
    with col2:
        height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01, key="bmi_height")
    
    with col3:
        if st.button("Calcular IMC", use_container_width=True):
            bmi = calculate_bmi(weight, height)
            category, color = get_bmi_category(bmi)
            
            st.metric("Seu IMC", f"{bmi}")
            st.markdown(f"**Classificação:** <span style='color: {color}'>{category}</span>", unsafe_allow_html=True)
    
    # Tabela de referência IMC
    st.markdown("#### 📊 Tabela de Referência IMC")
    
    imc_ref = pd.DataFrame({
        "Classificação": ["Abaixo do peso", "Peso normal", "Sobrepeso", "Obesidade Grau I", "Obesidade Grau II", "Obesidade Grau III"],
        "IMC": ["< 18,5", "18,5 - 24,9", "25,0 - 29,9", "30,0 - 34,9", "35,0 - 39,9", "≥ 40,0"],
        "Risco": ["Elevado", "Normal", "Levemente elevado", "Moderado", "Severo", "Muito severo"]
    })
    
    st.dataframe(imc_ref, use_container_width=True, hide_index=True)

def show_ideal_weight_calculator():
    """Calculadora de peso ideal"""
    st.markdown("### 🎯 Calculadora de Peso Ideal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01, key="ideal_height")
        sex = st.selectbox("Sexo", ["Masculino", "Feminino"], key="ideal_sex")
    
    with col2:
        if st.button("Calcular Peso Ideal", use_container_width=True):
            ideal_weights = calculate_ideal_weight(height, sex)
            
            st.markdown("#### 📊 Resultados por Fórmula")
            
            for formula, weight in ideal_weights.items():
                st.metric(f"Fórmula de {formula}", f"{weight} kg")
            
            # Média das fórmulas
            average_weight = sum(ideal_weights.values()) / len(ideal_weights)
            st.metric("**Peso Ideal Médio**", f"{average_weight:.1f} kg")
    
    # Informações sobre as fórmulas
    with st.expander("ℹ️ Sobre as Fórmulas"):
        st.markdown("""
        **Fórmula de Robinson (1983):**
        - Homens: 52 kg + 1,9 kg para cada 2,54 cm acima de 152,4 cm
        - Mulheres: 49 kg + 1,7 kg para cada 2,54 cm acima de 152,4 cm
        
        **Fórmula de Miller (1983):**
        - Homens: 56,2 kg + 1,41 kg para cada 2,54 cm acima de 152,4 cm
        - Mulheres: 53,1 kg + 1,36 kg para cada 2,54 cm acima de 152,4 cm
        
        **Fórmula de Devine (1974):**
        - Homens: 50 kg + 2,3 kg para cada 2,54 cm acima de 152,4 cm
        - Mulheres: 45,5 kg + 2,3 kg para cada 2,54 cm acima de 152,4 cm
        """)

def show_macro_calculator():
    """Calculadora de macronutrientes"""
    st.markdown("### 🥗 Calculadora de Macronutrientes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        calories = st.number_input("Calorias totais/dia", min_value=800, max_value=5000, value=2000, step=50)
        
        st.markdown("#### Distribuição de Macronutrientes (%)")
        carb_percent = st.slider("Carboidratos", min_value=0, max_value=100, value=50)
        protein_percent = st.slider("Proteínas", min_value=0, max_value=100, value=20)
        fat_percent = st.slider("Gorduras", min_value=0, max_value=100, value=30)
        
        total_percent = carb_percent + protein_percent + fat_percent
        
        if total_percent != 100:
            st.warning(f"⚠️ Total atual: {total_percent}%. Ajuste para 100%.")
        else:
            st.success("✅ Distribuição balanceada!")
    
    with col2:
        if total_percent == 100:
            macros = calculate_macros(calories, carb_percent, protein_percent, fat_percent)
            
            st.markdown("#### 📊 Resultado em Gramas")
            
            st.metric("Carboidratos", f"{macros['carboidratos']} g", f"{carb_percent}%")
            st.metric("Proteínas", f"{macros['proteinas']} g", f"{protein_percent}%")
            st.metric("Gorduras", f"{macros['gorduras']} g", f"{fat_percent}%")
            
            # Gráfico de pizza
            fig = px.pie(
                values=[carb_percent, protein_percent, fat_percent],
                names=['Carboidratos', 'Proteínas', 'Gorduras'],
                color_discrete_sequence=['#FF9999', '#66B2FF', '#99FF99'],
                title="Distribuição de Macronutrientes"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Recomendações padrão
    st.markdown("#### 💡 Recomendações por Objetivo")
    
    recommendations = {
        "Perda de Peso": {"carb": "40-45%", "protein": "25-30%", "fat": "25-30%"},
        "Ganho de Massa": {"carb": "45-55%", "protein": "20-25%", "fat": "20-30%"},
        "Manutenção": {"carb": "45-55%", "protein": "15-20%", "fat": "25-35%"},
        "Atletas": {"carb": "55-65%", "protein": "15-20%", "fat": "20-25%"}
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    for i, (objetivo, values) in enumerate(recommendations.items()):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"**{objetivo}**")
            st.write(f"Carboidratos: {values['carb']}")
            st.write(f"Proteínas: {values['protein']}")
            st.write(f"Gorduras: {values['fat']}")

def show_water_calculator():
    """Calculadora de necessidade hídrica"""
    st.markdown("### 💧 Calculadora de Hidratação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Peso (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1, key="water_weight")
        activity_level = st.selectbox(
            "Nível de Atividade",
            ["Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo", "Extremamente ativo"],
            key="water_activity"
        )
        
        climate = st.selectbox("Clima", ["Temperado", "Quente", "Muito quente"])
        
    with col2:
        if st.button("Calcular Necessidade Hídrica", use_container_width=True):
            water_ml = calculate_water_needs(weight, activity_level)
            
            # Ajuste por clima
            climate_factors = {"Temperado": 1.0, "Quente": 1.2, "Muito quente": 1.4}
            water_ml *= climate_factors[climate]
            
            water_liters = water_ml / 1000
            glasses = water_ml / 200  # Considerando copo de 200ml
            
            st.metric("Necessidade Diária", f"{water_ml:.0f} ml")
            st.metric("Em Litros", f"{water_liters:.1f} L")
            st.metric("Copos de 200ml", f"{glasses:.0f} copos")
            
            # Dicas de hidratação
            st.markdown("#### 💡 Dicas de Hidratação")
            st.write("• Beba um copo de água ao acordar")
            st.write("• Mantenha uma garrafa sempre próxima")
            st.write("• Beba antes de sentir sede")
            st.write("• Aumente o consumo durante exercícios")
            st.write("• Monitore a cor da urina (deve ser clara)")

def show_body_fat_calculator():
    """Calculadora de percentual de gordura corporal"""
    st.markdown("### 📊 Calculadora de Gordura Corporal")
    
    method = st.selectbox("Método de Cálculo", ["Fórmula do Exército Americano", "Fórmula da Marinha"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        sex = st.selectbox("Sexo", ["Masculino", "Feminino"], key="bf_sex")
        weight = st.number_input("Peso (kg)", min_value=20.0, max_value=300.0, value=70.0, key="bf_weight")
        height = st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, value=170.0, key="bf_height")
        
        if method == "Fórmula do Exército Americano":
            waist = st.number_input("Circunferência da Cintura (cm)", min_value=50.0, max_value=200.0, value=80.0)
            if sex == "Feminino":
                hip = st.number_input("Circunferência do Quadril (cm)", min_value=60.0, max_value=200.0, value=90.0)
                neck = st.number_input("Circunferência do Pescoço (cm)", min_value=20.0, max_value=60.0, value=35.0)
    
    with col2:
        if st.button("Calcular Gordura Corporal", use_container_width=True):
            # Cálculo simplificado (fórmulas completas seriam mais complexas)
            if sex == "Masculino":
                body_fat = 86.010 * math.log10(waist - neck) - 70.041 * math.log10(height) + 36.76
            else:
                body_fat = 163.205 * math.log10(waist + hip - neck) - 97.684 * math.log10(height) - 78.387
            
            body_fat = max(0, min(50, body_fat))  # Limitar entre 0-50%
            
            st.metric("Percentual de Gordura", f"{body_fat:.1f}%")
            
            # Classificação
            if sex == "Masculino":
                if body_fat < 6:
                    category = "Essencial"
                elif body_fat < 14:
                    category = "Atlético"
                elif body_fat < 18:
                    category = "Fitness"
                elif body_fat < 25:
                    category = "Aceitável"
                else:
                    category = "Obesidade"
            else:
                if body_fat < 14:
                    category = "Essencial"
                elif body_fat < 21:
                    category = "Atlético"
                elif body_fat < 25:
                    category = "Fitness"
                elif body_fat < 32:
                    category = "Aceitável"
                else:
                    category = "Obesidade"
            
            st.markdown(f"**Classificação:** {category}")

def show_calculators():
    """Função principal das calculadoras"""
    st.markdown("""
    <div style='background: linear-gradient(90deg, #4CAF50, #45a049); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>🧮 Calculadoras Nutricionais</h1>
        <p style='color: white; margin: 0; opacity: 0.9;'>Ferramentas essenciais para avaliação nutricional</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seletor de calculadora
    calculator_options = [
        "TMB e GET",
        "IMC",
        "Peso Ideal",
        "Macronutrientes",
        "Hidratação",
        "Gordura Corporal"
    ]
    
    selected_calculator = st.selectbox(
        "Escolha a calculadora:",
        calculator_options,
        index=0
    )
    
    st.divider()
    
    # Exibir calculadora selecionada
    if selected_calculator == "TMB e GET":
        show_bmr_calculator()
    elif selected_calculator == "IMC":
        show_bmi_calculator()
    elif selected_calculator == "Peso Ideal":
        show_ideal_weight_calculator()
    elif selected_calculator == "Macronutrientes":
        show_macro_calculator()
    elif selected_calculator == "Hidratação":
        show_water_calculator()
    elif selected_calculator == "Gordura Corporal":
        show_body_fat_calculator()
    
    # Informações adicionais
    st.markdown("---")
    
    with st.expander("ℹ️ Informações Importantes"):
        st.markdown("""
        **⚠️ Aviso Importante:**
        
        Estas calculadoras são ferramentas auxiliares e os resultados são estimativas baseadas em fórmulas científicas estabelecidas. 
        
        **Limitações:**
        - Não consideram composição corporal específica
        - Podem não ser precisas para atletas ou pessoas com composição corporal atípica
        - Não substituem avaliação profissional completa
        
        **Recomendações:**
        - Use sempre em conjunto com avaliação clínica
        - Considere o contexto individual de cada paciente
        - Para casos específicos, procure métodos de avaliação mais precisos
        
        **Para nutricionistas:** Estas ferramentas devem complementar, não substituir, sua avaliação profissional.
        """)

if __name__ == "__main__":
    show_calculators()