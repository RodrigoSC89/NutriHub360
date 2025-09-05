[readme_md.md](https://github.com/user-attachments/files/22175690/readme_md.md)
# NutriApp360 - Sistema Completo de Gestão Nutricional

Sistema integrado para gestão nutricional desenvolvido em Python com Streamlit, oferecendo interface moderna e funcionalidades completas para nutricionistas, pacientes e administradores.

## Características Principais

- **Sistema Multi-Perfil**: 7 tipos diferentes de usuário com permissões específicas
- **Dashboard Interativo**: Visualizações personalizadas para cada perfil
- **Gestão de Pacientes**: Cadastro completo com histórico e acompanhamento
- **Planos Alimentares**: Criação personalizada com cálculos nutricionais automáticos
- **Calculadoras Nutricionais**: TMB, IMC, macronutrientes, hidratação e mais
- **Sistema de Segurança**: Autenticação com hash e controle de permissões
- **Backup Automático**: Proteção e recuperação de dados
- **Interface Responsiva**: Compatível com desktop e dispositivos móveis

## Tipos de Usuário

1. **Administrador** - Gestão completa do sistema
2. **Nutricionista Senior** - Recursos avançados + supervisão de equipe
3. **Nutricionista Pleno** - Gestão completa de pacientes
4. **Nutricionista Junior** - Atendimento supervisionado
5. **Paciente** - Portal pessoal com plano e acompanhamento
6. **Recepcionista** - Agendamentos e cadastros
7. **Estagiário** - Acesso educacional e calculadoras

## Requisitos do Sistema

### Requisitos Mínimos
- **Python**: 3.8 ou superior
- **Sistema Operacional**: Windows 10, macOS 10.14, ou Linux Ubuntu 18.04+
- **RAM**: 4GB mínimo, 8GB recomendado
- **Armazenamento**: 500MB de espaço livre
- **Navegador**: Chrome, Firefox, Safari ou Edge (versão recente)

### Dependências Python
- streamlit >= 1.35.0
- pandas >= 2.2.0
- plotly >= 5.20.0
- python-dateutil >= 2.8.2
- matplotlib >= 3.8.0
- fpdf2 >= 2.7.9
- watchdog >= 3.0.0

## Instalação

### Instalação Automática (Recomendada)

1. **Baixar arquivos do sistema**
2. **Executar instalação automática:**
   ```bash
   python install.py
   ```

3. **Iniciar o sistema:**
   - Windows: Execute `run.bat`
   - Linux/Mac: Execute `./run.sh`
   - Ou manualmente: `python -m streamlit run main.py`

### Instalação Manual

1. **Preparar ambiente:**
   ```bash
   # Criar ambiente virtual (recomendado)
   python -m venv nutriapp360_env
   
   # Ativar ambiente virtual
   # Windows:
   nutriapp360_env\Scripts\activate
   # Linux/Mac:
   source nutriapp360_env/bin/activate
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Estrutura de arquivos necessária:**
   ```
   nutriapp360/
   ├── main.py
   ├── requirements.txt
   ├── install.py
   ├── .streamlit/
   │   └── config.toml
   ├── data/
   │   ├── users.json
   │   ├── patients.json
   │   └── appointments.json
   ├── modules/
   │   ├── __init__.py
   │   ├── admin_config.py
   │   ├── patient_dashboard.py
   │   ├── calculators.py
   │   ├── meal_plans.py
   │   ├── patient_management.py
   │   └── nutritionist_dashboard.py
   └── backups/
   ```

4. **Executar sistema:**
   ```bash
   streamlit run main.py
   ```

## Primeiro Acesso

### Credenciais Padrão
- **Usuário:** `admin`
- **Senha:** `admin123`

**IMPORTANTE:** Altere a senha padrão imediatamente após o primeiro login!

### Configuração Inicial

1. **Acesse como administrador**
2. **Vá para Configurações do Sistema**
3. **Configure:**
   - Nome da clínica/consultório
   - Número máximo de usuários
   - Configurações de segurança
   - Backup automático

4. **Criar primeiro usuário nutricionista:**
   - Acesse "Gestão de Usuários"
   - Clique "Novo Usuário"
   - Preencha dados profissionais
   - Defina tipo apropriado

## Uso do Sistema

### Para Administradores

**Dashboard Principal:**
- Visão geral do sistema
- Estatísticas de uso
- Status dos serviços
- Alertas importantes

**Gestão de Usuários:**
- Criar/editar usuários
- Definir permissões
- Suspender/ativar contas
- Histórico de acessos

**Configurações:**
- Parâmetros do sistema
- Políticas de segurança
- Configurações de backup
- Manutenção

### Para Nutricionistas

**Dashboard Profissional:**
- Métricas de pacientes
- Consultas do dia
- Evolução geral
- Ações rápidas

**Gestão de Pacientes:**
- Cadastro completo
- Histórico médico
- Dados antropométricos
- Acompanhamento

**Planos Alimentares:**
- Criação personalizada
- Banco de alimentos
- Cálculos automáticos
- Templates reutilizáveis

**Calculadoras:**
- TMB e GET
- IMC e peso ideal
- Macronutrientes
- Necessidade hídrica
- Percentual de gordura

### Para Pacientes

**Dashboard Pessoal:**
- Progresso visual
- Plano do dia
- Próxima consulta
- Conquistas

**Diário Alimentar:**
- Registro rápido
- Controle de hidratação
- Histórico completo
- Análise nutricional

**Acompanhamento:**
- Evolução de peso
- Adesão ao plano
- Humor e energia
- Comunicação

## Funcionalidades Detalhadas

### Sistema de Autenticação
- Hash SHA-256 para senhas
- Controle de sessão
- Tentativas de login limitadas
- Logout automático

### Gestão de Dados
- Armazenamento JSON (desenvolvimento)
- Cache inteligente
- Backup automático
- Recuperação de dados

### Calculadoras Nutricionais

**TMB (Taxa Metabólica Basal):**
- Equação Harris-Benedict revisada
- Fatores de atividade
- Recomendações por objetivo

**IMC (Índice de Massa Corporal):**
- Cálculo automático
- Classificação por faixas
- Referências atualizadas

**Peso Ideal:**
- Múltiplas fórmulas
- Comparação de métodos
- Faixas de referência

**Macronutrientes:**
- Distribuição personalizada
- Cálculo em gramas
- Visualização gráfica

**Hidratação:**
- Necessidade por peso
- Fatores de atividade
- Ajustes climáticos

### Relatórios e Analytics
- Evolução de pacientes
- Estatísticas de adesão
- Performance profissional
- Exportação de dados

## Segurança

### Medidas Implementadas
- Senhas com hash criptográfico
- Controle de permissões por perfil
- Logs de auditoria
- Backup seguro
- Sessões protegidas

### Boas Práticas
1. **Senhas fortes**: Mínimo 8 caracteres, números e símbolos
2. **Backup regular**: Configure backup automático
3. **Atualizações**: Mantenha sistema atualizado
4. **Monitoramento**: Verifique logs regularmente
5. **Acesso controlado**: Gerencie permissões adequadamente

## Backup e Recuperação

### Backup Automático
- Configurável por frequência
- Múltiplos tipos de dados
- Compressão opcional
- Notificações por email

### Recuperação Manual
1. Acesse "Painel Admin > Backup"
2. Selecione backup desejado
3. Escolha dados para restaurar
4. Confirme operação

**ATENÇÃO:** Backup sobrescreve dados atuais!

## Solução de Problemas

### Problemas Comuns

**Sistema não inicia:**
```bash
# Verificar Python
python --version

# Verificar Streamlit
streamlit --version

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

**Página em branco:**
- Verificar console do navegador (F12)
- Limpar cache do navegador
- Tentar outro navegador
- Verificar firewall/antivírus

**Erro de permissão:**
```bash
# Linux/Mac
chmod -R 755 data/

# Windows: Executar como administrador
```

**Dados não salvam:**
- Verificar permissões de escrita
- Verificar espaço em disco
- Verificar se diretório 'data/' existe

### Logs de Debug

**Ativar modo debug:**
```python
# No main.py, adicionar:
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Logs verbosos do Streamlit:**
```bash
streamlit run main.py --logger.level debug
```

## Performance

### Otimizações
- Cache do Streamlit ativo
- Carregamento lazy de dados
- Compressão de arquivos
- Limpeza automática

### Recomendações
- Usar ambiente virtual
- Limitar número de usuários simultâneos
- Configurar cache adequadamente
- Fazer manutenção regular

## Desenvolvimento

### Contribuindo

1. **Fork do projeto**
2. **Criar branch para feature**
3. **Implementar mudanças**
4. **Testes adequados**
5. **Pull request**

### Estrutura do Código

**main.py**: Aplicação principal e roteamento
**modules/**: Funcionalidades específicas
**data/**: Armazenamento de dados
**.streamlit/**: Configurações do framework

### Extensões Futuras
- Banco de dados PostgreSQL
- API REST
- App mobile nativo
- Integração com wearables
- IA para recomendações
- Multi-idioma

## Suporte

### Documentação
- README.md (este arquivo)
- Código comentado
- Docstrings nas funções

### Contato
- **Email**: nutriapp360@sistema.com
- **Suporte Técnico**: suporte@nutriapp360.com
- **Documentação Online**: docs.nutriapp360.com

### FAQ

**P: Posso usar em múltiplos computadores?**
R: Sim, mas dados ficam locais. Para sincronização, considere banco de dados compartilhado.

**P: Quantos usuários suporta?**
R: Por padrão 100 usuários, configurável pelo administrador.

**P: É possível personalizar interface?**
R: Sim, através do arquivo `.streamlit/config.toml` e CSS customizado.

**P: Como migrar para banco de dados?**
R: Substitua funções de load/save JSON por conexões com PostgreSQL, MySQL ou SQLite.

## Licença

Este projeto está sob licença MIT. Veja arquivo LICENSE para detalhes.

## Changelog

### Versão 1.0.0 (2024-09-04)
- Sistema de autenticação e perfis
- Dashboard para nutricionistas e pacientes
- Gestão completa de pacientes
- Criação de planos alimentares
- Calculadoras nutricionais
- Sistema de backup
- Painel administrativo
- Documentação completa

---

**© 2024 NutriApp360 - Sistema Completo de Gestão Nutricional**

*Desenvolvido para profissionais de nutrição comprometidos com a excelência no cuidado.*
