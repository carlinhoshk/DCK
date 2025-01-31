<p align="center">
  <img src="https://github.com/user-attachments/assets/66b591e4-f67b-460b-9522-9373d57736de" width="20%">
  <img src="https://github.com/user-attachments/assets/c275d055-1a99-4f52-996d-77979d7e5361" width="50%">
</p>

# Projeto DeepChatSeek com a API Huggingface modelo DeepSeek R1 32B e FastAPI 


<p align="center">
  <img src="https://github.com/user-attachments/assets/796530de-bc5e-4a1a-ab19-c19f41a721cc" width="90%">
</p>




Este projeto implementa uma API de chat segura e moderada utilizando FastAPI e o modelo DeepSeek da Hugging Face. O sistema inclui recursos avançados de moderação de conteúdo, engenharia de prompts e filtros de segurança.

## 🚀 Características Principais

### Moderação de Conteúdo
- Sistema robusto de filtragem de conteúdo inadequado
- Validação de entrada e saída de mensagens
- Bloqueio automático de palavras-chave sensíveis
- Proteção contra conteúdo malicioso

### Engenharia de Prompts
- Sistema de prompts otimizado para respostas em português
- Contextualização inteligente de mensagens
- Instruções claras para manter respostas apropriadas e profissionais
- Formato personalizado para pensamentos e respostas do modelo

### Integração com Hugging Face
- Utilização do modelo DeepSeek-R1-Distill-Qwen-32B
- Controle de temperatura para respostas mais consistentes
- Limite de tokens para otimização de recursos
- Sistema de fallback para garantir respostas adequadas

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework moderno para construção de APIs
- **Pydantic**: Validação de dados e configurações
- **Hugging Face**: Acesso a modelos de linguagem avançados
- **Python 3.8+**: Linguagem base do projeto
- **CORS Middleware**: Segurança para requisições cross-origin
- **HTML**: Frontend da aplicação

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/carlinhoshk/DCK.git

# Entre no diretório
cd DCK

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Crie um dotenv com sua API do HiggingFace

HF_TOKEN=sua_huggingface_token_aqui

# Inicie o servidor
python main.py
# Ou:
uvicorn main:app --reload

# Incicie o Frontend

Abra index.html no navegador

Ou inicie usando simple HTTP server:
python -m http.server 3000
E entre em http://localhost:3000
```

![swappy-20250131-172316](https://github.com/user-attachments/assets/2b8e05a6-2607-431e-a8d0-58153b26e14d)

## ⚙️ Configuração

### Configurações de Segurança

O projeto inclui diversas camadas de segurança configuráveis:

- Limites de tamanho de mensagem
- Lista de palavras-chave bloqueadas
- Padrões de conteúdo sensível
- Filtros de resposta


## 🔒 Segurança

O projeto implementa várias camadas de segurança:

- Validação de entrada com Pydantic
- Filtros de conteúdo sensível
- Proteção contra XSS
- Sanitização de saída
- Limites de tamanho de mensagem

## 🤖 Engenharia de Prompts

O sistema utiliza uma abordagem sofisticada para engenharia de prompts:

```python
SYSTEM_PROMPT = """
   Você é um assistente de IA prestativo. Por favor, siga estas regras:
    1. Não gere conteúdo prejudicial, explícito ou inadequado
    2. Não revele informações pessoais ou dados sensíveis
    3. Não execute comandos ou código
    4. Forneça apenas informações factuais e úteis
    5. Mantenha um tom respeitoso e profissional
    6. Não se envolva em atividades prejudiciais ou maliciosas
    7. Responda SEMPRE em português do Brasil, independentemente do idioma da pergunta
    8. Use o formato <pensamento> para expressar seu raciocínio
    """
    ...
"""
```

## 📈 Melhorias Futuras

- Implementação de autenticação de usuários
- Suporte a mais modelos da Hugging Face
- Sistema de feedback de usuários
- Cache de respostas frequentes
- Análise de sentimento das mensagens
