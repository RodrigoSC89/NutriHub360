# modules/patient_management.py
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go

class PatientManager:
    def __init__(self):
        self.data_file = 'data/patients.json'
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Garante que o diretório de dados existe"""
        os.makedirs('data', exist_ok=True)
    
    @st.cache_data
    def load_patients(_self):
        """Carrega dados dos pacientes"""
        if os.path.exists(_self.data_file):
            with open(_self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_patients(self, patients_data):
        """Salva dados dos pacientes"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(patients_data, f, indent=2, ensure_ascii=False, default=str)
    
    def add_patient(self, patient_data):
        """Adiciona novo paciente"""
        patients = self.load_patients()
        patient_id = f"PAC_{len(patients) + 1:04d}"
        patient_data['id'] = patient_id
        patient_data['created_at'] = datetime.now().isoformat()
        patient_data['updated_at'] = datetime.now().isoformat()
        patients[patient_id] = patient_data
        self.save_patients(patients)
        return patient_id
    
    def update_patient(self, patient_id, patient_data):
        """Atualiza dados do paciente"""
        patients = self.load_patients()
        if patient_id in patients:
            patient_data['updated_at'] = datetime.now().isoformat()
            patients[patient_id] = {**patients[patient_id], **patient_data}
            self.save_patients(patients)
            return True
        return False
    
    def get_patient(self, patient_id):
        """Obtém dados de um paciente específico"""
        patients = self.load_patients()
        return patients.get(patient_id)
    
    def delete_patient(self, patient_id):
        """Remove paciente (soft delete)"""
        patients = self.load_patients()
        if patient_id in patients:
            patients[patient_id]['status'] = 'inativo'
            patients[patient_id]['updated_at'] = datetime.now().isoformat()
            self.save_patients(patients)
            return True
        return False

def show_patient_form(patient_data=None):
    """Formulário para cadastro/edição de paciente"""
    is_edit = patient_data is not None
    
    st.markdown(f"### {'✏️ Editar' if is_edit else '➕ Novo'} Paciente")
    
    with st.form("patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input(
                "Nome Completo *", 
                value=patient_data.get('nome', '') if is_edit else ''
            )
            
            cpf = st.text_input(
                "CPF", 
                value=patient_data.get('cpf', '') if is_edit else ''
            )
            
            data_nascimento = st.date_input(
                "Data de Nascimento *",
                value=datetime.fromisoformat(patient_data.get('data_nascimento', '1990-01-01')).date() if is_edit else date(1990, 1, 1)
            )
            
            sexo = st.selectbox(
                "Sexo *",
                ['Feminino', 'Masculino', 'Outro'],
                index=['Feminino', 'Masculino', 'Outro'].index(patient_data.get('sexo', 'Feminino')) if is_edit else 0
            )
            
            telefone = st.text_input(
                "Telefone *",
                value=patient_data.get('telefone', '') if is_edit else ''
            )
        
        with col2:
            email = st.text_input(
                "E-mail",
                value=patient_data.get('email', '') if is_edit else ''
            )
            
            endereco = st.text_area(
                "Endereço",
                value=patient_data.get('endereco', '') if is_edit else ''
            )
            
            profissao = st.text_input(
                "Profissão",
                value=patient_data.get('profissao', '') if is_edit else ''
            )
            
            objetivo = st.selectbox(
                "Objetivo Principal *",
                ['Perda de peso', 'Ganho de peso', 'Manutenção', 'Ganho de massa muscular', 'Saúde geral'],
                index=['Perda de peso', 'Ganho de peso', 'Manutenção', 'Ganho de massa muscular', 'Saúde geral'].index(patient_data.get('objetivo', 'Perda de peso')) if is_edit else 0
            )
        
        st.markdown("#### 📊 Dados Antropométricos")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            peso = st.number_input(
                "Peso (kg) *", 
                min_value=20.0, 
                max_value=300.0, 
                step=0.1,
                value=float(patient_data.get('peso', 70.0)) if is_edit else 70.0
            )
        
        with col4:
            altura = st.number_input(
                "Altura (m) *", 
                min_value=1.0, 
                max_value=2.5, 
                step=0.01,
                value=float(patient_data.get('altura', 1.70)) if is_edit else 1.70
            )
        
        with col5:
            # Cálculo automático do IMC
            imc = peso / (altura ** 2) if altura > 0 else 0
            st.metric("IMC Calculado", f"{imc:.1f}")
        
        st.markdown("#### 🏥 Informações Médicas")
        col6, col7 = st.columns(2)
        
        with col6:
            condicoes_medicas = st.text_area(
                "Condições Médicas",
                value=patient_data.get('condicoes_medicas', '') if is_edit else '',
                help="Diabetes, hipertensão, alergias, etc."
            )
            
            medicamentos = st.text_area(
                "Medicamentos em Uso",
                value=patient_data.get('medicamentos', '') if is_edit else ''
            )
        
        with col7:
            alergias_alimentares = st.text_area(
                "Alergias/Intolerâncias Alimentares",
                value=patient_data.get('alergias_alimentares', '') if is_edit else ''
            )
            
            observacoes = st.text_area(
                "Observações Gerais",
                value=patient_data.get('observacoes', '') if is_edit else ''
            )
        
        # Botões do formulário
        col_cancel, col_submit = st.columns([1, 1])
        
        with col_cancel:
            cancel_button = st.form_submit_button("❌ Cancelar", use_container_width=True)
        
        with col_submit:
            submit_button = st.form_submit_button(
                f"💾 {'Atualizar' if is_edit else 'Cadastrar'}", 
                use_container_width=True,
                type="primary"
            )
        
        if cancel_button:
            st.session_state.show_patient_form = False
            st.rerun()
        
        if submit_button:
            # Validações
            if not nome or not telefone or not data_nascimento:
                st.error("Por favor, preencha todos os campos obrigatórios (*).")
            else:
                # Preparar dados
                patient_info = {
                    'nome': nome,
                    'cpf': cpf,
                    'data_nascimento': data_nascimento.isoformat(),
                    'sexo': sexo,
                    'telefone': telefone,
                    'email': email,
                    'endereco': endereco,
                    'profissao': profissao,
                    'objetivo': objetivo,
                    'peso': peso,
                    'altura': altura,
                    'imc': round(imc, 1),
                    'condicoes_medicas': condicoes_medicas,
                    'medicamentos': medicamentos,
                    'alergias_alimentares': alergias_alimentares,
                    'observacoes': observacoes,
                    'status': 'ativo'
                }
                
                # Salvar dados
                manager = PatientManager()
                
                if is_edit:
                    if manager.update_patient(patient_data['id'], patient_info):
                        st.success("✅ Paciente atualizado com sucesso!")
                    else:
                        st.error("❌ Erro ao atualizar paciente.")
                else:
                    patient_id = manager.add_patient(patient_info)
                    st.success(f"✅ Paciente cadastrado com sucesso! ID: {patient_id}")
                
                st.session_state.show_patient_form = False
                st.rerun()

def show_patient_list():
    """Exibe lista de pacientes"""
    manager = PatientManager()
    patients = manager.load_patients()
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_name = st.text_input("🔍 Buscar por nome")
    
    with col2:
        filter_objective = st.selectbox(
            "Filtrar por objetivo",
            ['Todos', 'Perda de peso', 'Ganho de peso', 'Manutenção', 'Ganho de massa muscular', 'Saúde geral']
        )
    
    with col3:
        filter_status = st.selectbox(
            "Status",
            ['Todos', 'ativo', 'inativo']
        )
    
    with col4:
        if st.button("➕ Novo Paciente", use_container_width=True):
            st.session_state.show_patient_form = True
            st.session_state.edit_patient = None
            st.rerun()
    
    # Processar dados para exibição
    if patients:
        patients_list = []
        for patient_id, patient_data in patients.items():
            # Aplicar filtros
            if search_name and search_name.lower() not in patient_data.get('nome', '').lower():
                continue
            
            if filter_objective != 'Todos' and patient_data.get('objetivo') != filter_objective:
                continue
            
            if filter_status != 'Todos' and patient_data.get('status', 'ativo') != filter_status:
                continue
            
            # Calcular idade
            nascimento = datetime.fromisoformat(patient_data.get('data_nascimento', '1990-01-01'))
            idade = (datetime.now() - nascimento).days // 365
            
            patients_list.append({
                'ID': patient_id,
                'Nome': patient_data.get('nome', ''),
                'Idade': idade,
                'Sexo': patient_data.get('sexo', ''),
                'Objetivo': patient_data.get('objetivo', ''),
                'IMC': patient_data.get('imc', 0),
                'Telefone': patient_data.get('telefone', ''),
                'Status': patient_data.get('status', 'ativo'),
                'Última Atualização': patient_data.get('updated_at', '')[:10] if patient_data.get('updated_at') else ''
            })
        
        if patients_list:
            df = pd.DataFrame(patients_list)
            
            # Configurar exibição da tabela
            st.markdown(f"### 👥 Pacientes ({len(patients_list)} encontrado{'s' if len(patients_list) != 1 else ''})")
            
            # Exibir tabela com ações
            for idx, patient in enumerate(patients_list):
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
                    
                    with col1:
                        st.markdown(f"**{patient['Nome']}**")
                        st.caption(f"ID: {patient['ID']} | {patient['Idade']} anos | {patient['Objetivo']}")
                    
                    with col2:
                        st.metric("IMC", f"{patient['IMC']}")
                    
                    with col3:
                        status_color = "🟢" if patient['Status'] == 'ativo' else "🔴"
                        st.markdown(f"{status_color} {patient['Status'].title()}")
                    
                    with col4:
                        if st.button("👁️", key=f"view_{patient['ID']}", help="Visualizar"):
                            st.session_state.view_patient = patient['ID']
                            st.rerun()
                    
                    with col5:
                        col_edit, col_delete = st.columns(2)
                        with col_edit:
                            if st.button("✏️", key=f"edit_{patient['ID']}", help="Editar"):
                                st.session_state.show_patient_form = True
                                st.session_state.edit_patient = patient['ID']
                                st.rerun()
                        
                        with col_delete:
                            if st.button("🗑️", key=f"delete_{patient['ID']}", help="Inativar"):
                                if manager.delete_patient(patient['ID']):
                                    st.success("Paciente inativado!")
                                    st.rerun()
                    
                    st.divider()
        else:
            st.info("Nenhum paciente encontrado com os filtros aplicados.")
    else:
        st.info("Nenhum paciente cadastrado ainda.")

def show_patient_detail(patient_id):
    """Exibe detalhes de um paciente específico"""
    manager = PatientManager()
    patient = manager.get_patient(patient_id)
    
    if not patient:
        st.error("Paciente não encontrado!")
        return
    
    # Header do paciente
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"# 👤 {patient.get('nome', 'N/A')}")
        st.markdown(f"**ID:** {patient_id} | **Status:** {patient.get('status', 'ativo').title()}")
    
    with col2:
        if st.button("🔙 Voltar", use_container_width=True):
            st.session_state.view_patient = None
            st.rerun()
        
        if st.button("✏️ Editar", use_container_width=True):
            st.session_state.show_patient_form = True
            st.session_state.edit_patient = patient_id
            st.rerun()
    
    # Abas com informações
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Dados Gerais", "📊 Antropometria", "🏥 Médico", "📈 Evolução"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Informações Pessoais")
            st.write(f"**Nome:** {patient.get('nome', 'N/A')}")
            st.write(f"**CPF:** {patient.get('cpf', 'N/A')}")
            st.write(f"**Data de Nascimento:** {patient.get('data_nascimento', 'N/A')}")
            st.write(f"**Sexo:** {patient.get('sexo', 'N/A')}")
            st.write(f"**Telefone:** {patient.get('telefone', 'N/A')}")
            st.write(f"**E-mail:** {patient.get('email', 'N/A')}")
        
        with col2:
            st.markdown("#### 💼 Outras Informações")
            st.write(f"**Profissão:** {patient.get('profissao', 'N/A')}")
            st.write(f"**Objetivo:** {patient.get('objetivo', 'N/A')}")
            st.write(f"**Endereço:** {patient.get('endereco', 'N/A')}")
            st.write(f"**Cadastrado em:** {patient.get('created_at', 'N/A')[:10]}")
            st.write(f"**Última atualização:** {patient.get('updated_at', 'N/A')[:10]}")
    
    with tab2:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Peso", f"{patient.get('peso', 0)} kg")
        
        with col2:
            st.metric("Altura", f"{patient.get('altura', 0)} m")
        
        with col3:
            imc = patient.get('imc', 0)
            if imc < 18.5:
                imc_status = "Abaixo do peso"
                imc_color = "blue"
            elif imc < 25:
                imc_status = "Peso normal"
                imc_color = "green"
            elif imc < 30:
                imc_status = "Sobrepeso"
                imc_color = "orange"
            else:
                imc_status = "Obesidade"
                imc_color = "red"
            
            st.metric("IMC", f"{imc}", delta=imc_status)
    
    with tab3:
        st.markdown("#### 🏥 Informações Médicas")
        
        if patient.get('condicoes_medicas'):
            st.markdown("**Condições Médicas:**")
            st.write(patient.get('condicoes_medicas'))
        
        if patient.get('medicamentos'):
            st.markdown("**Medicamentos:**")
            st.write(patient.get('medicamentos'))
        
        if patient.get('alergias_alimentares'):
            st.markdown("**Alergias/Intolerâncias:**")
            st.write(patient.get('alergias_alimentares'))
        
        if patient.get('observacoes'):
            st.markdown("**Observações:**")
            st.write(patient.get('observacoes'))
    
    with tab4:
        st.markdown("#### 📈 Evolução do Paciente")
        st.info("Em desenvolvimento: Gráficos de evolução de peso, medidas e adesão ao tratamento.")

def show_patient_management():
    """Função principal da gestão de pacientes"""
    # Verificar se deve mostrar formulário
    if st.session_state.get('show_patient_form', False):
        patient_data = None
        if st.session_state.get('edit_patient'):
            manager = PatientManager()
            patient_data = manager.get_patient(st.session_state.edit_patient)
        
        show_patient_form(patient_data)
    
    # Verificar se deve mostrar detalhes
    elif st.session_state.get('view_patient'):
        show_patient_detail(st.session_state.view_patient)
    
    # Mostrar lista de pacientes
    else:
        st.markdown("""
        <div style='background: linear-gradient(90deg, #4CAF50, #45a049); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; margin: 0;'>👥 Gestão de Pacientes</h1>
            <p style='color: white; margin: 0; opacity: 0.9;'>Cadastre, edite e acompanhe seus pacientes</p>
        </div>
        """, unsafe_allow_html=True)
        
        show_patient_list()

# Inicializar estados da sessão
if 'show_patient_form' not in st.session_state:
    st.session_state.show_patient_form = False
if 'edit_patient' not in st.session_state:
    st.session_state.edit_patient = None
if 'view_patient' not in st.session_state:
    st.session_state.view_patient = None

if __name__ == "__main__":
    show_patient_management()