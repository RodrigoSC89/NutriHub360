[tutorial_complete.md](https://github.com/user-attachments/files/22163552/tutorial_complete.md)
# 🥗 NutriApp360 - Tutorial Completo de Instalação e Uso

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Requisitos do Sistema](#requisitos-do-sistema)
3. [Instalação](#instalação)
4. [Configuração Inicial](#configuração-inicial)
5. [Estrutura do Sistema](#estrutura-do-sistema)
6. [Guia de Uso por Perfil](#guia-de-uso-por-perfil)
7. [Funcionalidades Principais](#funcionalidades-principais)
8. [Administração do Sistema](#administração-do-sistema)
9. [Resolução de Problemas](#resolução-de-problemas)
10. [FAQ](#faq)

---

## 🎯 Visão Geral

O **NutriApp360** é um sistema completo de gestão nutricional desenvolvido em Python com Streamlit. Oferece uma plataforma integrada para nutricionistas, pacientes e administradores, com funcionalidades que incluem:

- ✅ **Gestão completa de pacientes**
- ✅ **Criação de planos alimentares personalizados**
- ✅ **Calculadoras nutricionais avançadas**
- ✅ **Sistema de perfis e permissões**
- ✅ **Dashboard interativo para cada tipo de usuário**
- ✅ **Acompanhamento de progresso em tempo real**
- ✅ **Sistema de backup e segurança**

---

## 💻 Requisitos do Sistema

### Requisitos Mínimos
- **Sistema Operacional:** Windows 10, macOS 10.14, ou Linux Ubuntu 18.04+
- **Python:** Versão 3.8 ou superior
- **RAM:** 4GB mínimo, 8GB recomendado
- **Armazenamento:** 500MB de espaço livre
- **Navegador:** Chrome, Firefox, Safari ou Edge (versão recente)

### Dependências Python
```text
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.17.0
hashlib (built-in)
json (built-in)
os (built-in)
datetime (built-in)
```

---

## 🚀 Instalação

### Passo 1: Preparação do Ambiente

#### 1.1 Instalar Python
```bash
# Verificar se Python está instalado
python --version

# Se não estiver instalado, baixar de: https://python.org
```

#### 1.2 Criar Ambiente Virtual (Recomendado)
```bash
# Criar ambiente virtual
python -m venv nutriapp360_env

# Ativar ambiente virtual
# Windows:
nutriapp360_env\Scripts\activate

# macOS/Linux:
source nutriapp360_env/bin/activate
```

### Passo 2: Instalação das Dependências

#### 2.1 Criar arquivo requirements.txt
```text
streamlit==1.28.0
pandas==1.5.3
plotly==5.17.0
```

#### 2.2 Instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Estrutura de Arquivos

#### 3.1 Criar estrutura de diretórios
```
nutriapp360/
├── main.py                    # Arquivo principal
├── requirements.txt           # Dependências
├── .streamlit/
│   └── config.toml           # Configurações do Streamlit
├── modules/                  # Módulos do sistema
│   ├── __init__.py
│   ├── nutritionist_dashboard.py
│   ├── patient_dashboard.py
│   ├── patient_management.py
│   ├── meal_plans.py
│   ├── calculators.py
│   └── admin_config.py
├── data/                     # Dados do sistema
│   ├── users.json
│   ├── patients.json
│   ├── meal_plans.json
│   └── system_config.json
└── backups/                  # Backups automáticos
```

#### 3.2 Criar arquivo de configuração Streamlit
**Arquivo: `.streamlit/config.toml`**
```toml
[server]
port = 8501
headless = false

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[browser]
gatherUsageStats = false
```

### Passo 4: Execução

#### 4.1 Executar o sistema
```bash
streamlit run main.py
```

#### 4.2 Acessar o sistema
- Abrir navegador em: `http://localhost:8501`
- O sistema iniciará automaticamente

---

## ⚙️ Configuração Inicial

### Primeira Execução

#### 1. Usuário Administrador Padrão
- **Usuário:** `admin`
- **Senha:** `admin123`
- ⚠️ **IMPORTANTE:** Altere a senha padrão imediatamente após o primeiro login

#### 2. Configurações Básicas
1. Acesse o **Painel de Administração**
2. Vá para **Configurações**
3. Configure:
   - Nome da clínica/consultório
   - Número máximo de usuários
   - Configurações de segurança
   - Backup automático

#### 3. Criar Primeiro Usuário Nutricionista
1. No painel admin, vá para **Gestão de Usuários**
2. Clique em **Novo Usuário**
3. Preencha os dados:
   - Nome de usuário
   - Senha
   - Tipo: `nutricionista_senior`
   - Dados do perfil (CRN, especialidade)

---

## 🏗️ Estrutura do Sistema

### Arquitetura de Perfis

#### 1. **Administrador (`admin`)**
- Gestão completa do sistema
- Configurações gerais
- Backup e restauração
- Logs e auditoria
- Gestão de usuários

#### 2. **Nutricionista Senior (`nutricionista_senior`)**
- Todos os recursos de nutricionista
- Supervisão de equipe
- Criação de protocolos
- Relatórios avançados

#### 3. **Nutricionista Pleno (`nutricionista_pleno`)**
- Gestão de pacientes
- Criação de planos alimentares
- Relatórios básicos
- Calculadoras

#### 4. **Nutricionista Junior (`nutricionista_junior`)**
- Atendimento supervisionado
- Planos com aprovação
- Acesso limitado

#### 5. **Paciente (`paciente`)**
- Visualização do próprio plano
- Diário alimentar
- Agendamento de consultas
- Acompanhamento de progresso

#### 6. **Recepcionista (`recepcionista`)**
- Agendamentos
- Cadastros básicos
- Controle financeiro

#### 7. **Estagiário (`estagiario`)**
- Acesso educacional
- Casos anonimizados
- Calculadoras
- Simulações

### Sistema de Permissões

```python
PERMISSIONS = {
    'admin': ['manage_users', 'view_all_data', 'system_config'],
    'nutricionista_senior': ['manage_patients', 'create_protocols', 'supervise_team'],
    'nutricionista_pleno': ['manage_patients', 'create_meal_plans', 'basic_reports'],
    'paciente': ['view_own_plan', 'food_diary', 'schedule_appointments']
    # ... outros perfis
}
```

---

## 👥 Guia de Uso por Perfil

### 🔧 Para Administradores

#### Acesso ao Sistema
1. Login com credenciais de admin
2. Acesso automático ao painel de administração

#### Principais Tarefas
- **Gestão de Usuários:**
  - Criar novos usuários
  - Editar permissões
  - Suspender/ativar contas

- **Configurações do Sistema:**
  - Ajustar parâmetros gerais
  - Configurar backup automático
  - Definir políticas de segurança

- **Monitoramento:**
  - Visualizar logs do sistema
  - Acompanhar métricas de uso
  - Status dos serviços

### 🥗 Para Nutricionistas

#### Acesso ao Sistema
1. Login com credenciais fornecidas pelo admin
2. Redirecionamento automático para dashboard

#### Dashboard Principal
- **Métricas:** Total de pacientes, consultas do dia, taxa de adesão
- **Ações Rápidas:** Novo paciente, criar plano, nova consulta
- **Alertas:** Pacientes sem registro, metas atingidas

#### Gestão de Pacientes
1. **Cadastrar Novo Paciente:**
   ```
   Menu → Pacientes → Novo Paciente
   ```
   - Preencher dados pessoais
   - Informações antropométricas
   - Histórico médico
   - Objetivos

2. **Acompanhar Paciente:**
   - Visualizar evolução
   - Ajustar planos
   - Registrar consultas

#### Criação de Planos Alimentares
1. **Novo Plano:**
   ```
   Menu → Planos Alimentares → Novo Plano
   ```
   - Selecionar paciente
   - Definir meta calórica
   - Escolher alimentos por refeição
   - Calcular macronutrientes automaticamente

2. **Recursos Avançados:**
   - Templates personalizáveis
   - Substituições automáticas
   - Cálculo nutricional em tempo real

#### Calculadoras Nutricionais
- **TMB e GET:** Taxa metabólica e gasto energético
- **IMC:** Índice de massa corporal
- **Peso Ideal:** Múltiplas fórmulas
- **Macronutrientes:** Distribuição personalizada
- **Hidratação:** Necessidade hídrica
- **Gordura Corporal:** Percentual estimado

### 👤 Para Pacientes

#### Acesso ao Sistema
1. Receber credenciais do nutricionista
2. Login no portal do paciente

#### Dashboard do Paciente
- **Progresso:** Evolução de peso, IMC, metas
- **Plano do Dia:** Refeições programadas
- **Próxima Consulta:** Data e horário
- **Conquistas:** Marcos alcançados

#### Diário Alimentar
1. **Registro Rápido:**
   - Selecionar refeição
   - Informar alimento
   - Especificar quantidade

2. **Controle de Hidratação:**
   - Meta diária
   - Registro por copos/garrafas
   - Progresso visual

#### Acompanhamento
- **Evolução de Peso:** Gráficos interativos
- **Adesão ao Plano:** Percentual de cumprimento
- **Humor e Energia:** Registro diário

### 📋 Para Recepcionistas

#### Funcionalidades Principais
- **Agendamentos:**
  - Visualizar agenda
  - Marcar consultas
  - Confirmar presença

- **Cadastros:**
  - Dados básicos de pacientes
  - Informações de contato
  - Documentação

- **Financeiro:**
  - Controle de pagamentos
  - Relatórios básicos
  - Faturas

---

## 🔧 Funcionalidades Principais

### Sistema de Autenticação
```python
# Exemplo de uso do sistema de autenticação
auth = AuthSystem()
user = auth.authenticate(username, password)
if user:
    st.session_state.authenticated = True
    st.session_state.user = user
```

### Gestão de Dados
- **Armazenamento:** JSON para prototipagem (migrar para DB em produção)
- **Cache:** Streamlit cache para performance
- **Backup:** Sistema automático de backup

### Cálculos Nutricionais
```python
# Exemplo de cálculo de TMB
def calculate_bmr(weight, height, age, sex):
    if sex == "Masculino":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return round(bmr, 1)
```

### Visualizações Interativas
- **Plotly:** Gráficos interativos
- **Métricas:** KPIs em tempo real
- **Dashboards:** Personalizados por perfil

---

## 🛠️ Administração do Sistema

### Backup e Recuperação

#### Backup Manual
1. Acesse **Painel Admin → Backup**
2. Selecione dados para backup
3. Defina nome do backup
4. Execute backup

#### Backup Automático
- **Configuração:** Admin → Configurações → Backup
- **Frequência:** Diário, semanal ou mensal
- **Horário:** Configurável
- **Retenção:** Definir por quantos dias manter

#### Restauração
1. Selecione backup disponível
2. Escolha dados para restaurar
3. **⚠️ ATENÇÃO:** Confirmação necessária (sobrescreve dados atuais)

### Monitoramento

#### Logs do Sistema
- **Acesso:** Admin → Logs
- **Filtros:** Por data, usuário, nível
- **Tipos:** Info, Warning, Error, Critical

#### Métricas de Performance
- Usuários ativos
- Uso de recursos
- Tempo de resposta
- Status dos serviços

### Segurança

#### Configurações de Segurança
```python
"security": {
    "password_min_length": 6,
    "session_encryption": True,
    "two_factor_auth": False,
    "login_attempts": 3
}
```

#### Boas Práticas
1. **Senhas Fortes:** Mínimo 8 caracteres, números e símbolos
2. **Backup Regular:** Configurar backup automático
3. **Atualizações:** Manter sistema atualizado
4. **Monitoramento:** Verificar logs regularmente

---

## 🔍 Resolução de Problemas

### Problemas Comuns

#### 1. Sistema não inicia
**Sintoma:** Erro ao executar `streamlit run main.py`

**Soluções:**
```bash
# Verificar instalação do Streamlit
pip list | grep streamlit

# Reinstalar se necessário
pip install --upgrade streamlit

# Verificar Python
python --version
```

#### 2. Página em branco
**Sintoma:** Sistema abre mas não carrega conteúdo

**Soluções:**
1. Verificar console do navegador (F12)
2. Limpar cache do navegador
3. Tentar outro navegador
4. Verificar firewall/antivírus

#### 3. Erro de permissão de arquivo
**Sintoma:** Erro ao salvar dados

**Soluções:**
```bash
# Verificar permissões do diretório
ls -la data/

# Corrigir permissões (Linux/Mac)
chmod -R 755 data/

# Windows: Executar como administrador
```

#### 4. Dados não salvam
**Sintoma:** Alterações não persistem

**Soluções:**
1. Verificar se diretório `data/` existe
2. Verificar permissões de escrita
3. Verificar espaço em disco
4. Reiniciar aplicação

### Logs de Debug

#### Ativar Modo Debug
```python
# No main.py, adicionar:
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Verificar Logs do Streamlit
```bash
# Executar com logs verbosos
streamlit run main.py --logger.level debug
```

### Performance

#### Otimização
1. **Cache:** Usar `@st.cache_data` adequadamente
2. **Dados:** Limitar quantidade de dados carregados
3. **Imagens:** Otimizar tamanho das imagens
4. **Sessão:** Limpar estados desnecessários

---

## ❓ FAQ

### Perguntas Gerais

**Q: O sistema funciona offline?**
A: Sim, o NutriApp360 é uma aplicação local que funciona sem internet.

**Q: Posso usar em múltiplos computadores?**
A: Sim, mas os dados ficarão locais em cada máquina. Para sincronização, considere usar um banco de dados compartilhado.

**Q: Quantos usuários suporta?**
A: Por padrão, 100 usuários, mas configurável pelo administrador.

**Q: É possível personalizar a interface?**
A: Sim, através do arquivo `.streamlit/config.toml` e CSS customizado.

### Perguntas Técnicas

**Q: Como migrar dados para banco de dados?**
A: Substitua as funções de load/save JSON por conexões com PostgreSQL, MySQL ou SQLite.

**Q: Como adicionar novos alimentos ao banco?**
A: Edite o arquivo `data/foods_database.json` ou crie interface administrativa.

**Q: É possível integrar com APIs externas?**
A: Sim, adicione as chamadas de API nos módulos relevantes.

**Q: Como fazer deploy em produção?**
A: Use Streamlit Cloud, Heroku, Docker ou servidor próprio com nginx.

### Suporte

**Q: Onde obter suporte?**
A: Este é um sistema de demonstração. Para suporte comercial, contate o desenvolvedor.

**Q: Como contribuir com melhorias?**
A: Fork o projeto, implemente melhorias e submeta pull request.

**Q: Licença de uso?**
A: Verifique arquivo LICENSE no repositório do projeto.

---

## 🚀 Próximos Passos

### Melhorias Futuras
1. **Banco de Dados:** Migração de JSON para PostgreSQL
2. **API REST:** Desenvolvimento de API para integrações
3. **App Mobile:** Versão nativa para iOS/Android
4. **Integrações:** Balança inteligente, wearables
5. **IA:** Recomendações automáticas de planos
6. **Multi-idioma:** Suporte a outros idiomas
7. **Telemedicina:** Videochamadas integradas

### Contribuições
- **Código:** Novos módulos e funcionalidades
- **Documentação:** Melhorias na documentação
- **Tradução:** Suporte a novos idiomas
- **Testes:** Casos de teste automatizados

---

## 📞 Contato e Suporte

Para dúvidas, sugestões ou suporte técnico:

- **E-mail:** suporte@nutriapp360.com
- **GitHub:** [github.com/nutriapp360](https://github.com/nutriapp360)
- **Documentação:** [docs.nutriapp360.com](https://docs.nutriapp360.com)

---

## 📝 Changelog

### Versão 1.0.0 (2024-09-04)
- ✅ Sistema de autenticação e perfis
- ✅ Dashboard para nutricionistas e pacientes
- ✅ Gestão completa de pacientes
- ✅ Criação de planos alimentares
- ✅ Calculadoras nutricionais
- ✅ Sistema de backup
- ✅ Painel administrativo
- ✅ Documentação completa

---

**© 2024 NutriApp360 - Sistema Completo de Gestão Nutricional**
