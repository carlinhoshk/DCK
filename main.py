from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import re
import json
from typing import List, Dict, Optional
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv(".env")


class SecurityConfig:
    # Validação de entrada
    MAX_MESSAGE_LENGTH = 2500
    MIN_MESSAGE_LENGTH = 1
    BLOCKED_KEYWORDS = {
        "sql",
        "exec",
        "eval",
        "system",
        "os.",
        "subprocess",
        "rm -rf",
        "format",
        "delete",
        "drop table",
    }

    # Moderação de conteúdo
    SENSITIVE_TOPICS = {
        "explicit_content": ["porn", "xxx", "nsfw"],
        "hate_speech": ["hate", "racist", "discrimination"],
        "violence": ["kill", "murder", "attack"],
        "personal_info": ["ssn", "credit card", "passport"],
    }

    # Validação de saída
    MAX_RESPONSE_LENGTH = 4096
    RESTRICTED_PATTERNS = [
        r"(?i)(password|secret|key):\s*\w+",  # Padrões de dados sensíveis
        r"(?i)(<script>|javascript:)",  # Padrões XSS
        r"(?i)(SELECT|INSERT|UPDATE|DELETE)\s+FROM",  # Padrões SQL
    ]


class ChatMessage(BaseModel):
    message: str = Field(
        ...,
        min_length=SecurityConfig.MIN_MESSAGE_LENGTH,
        max_length=SecurityConfig.MAX_MESSAGE_LENGTH,
    )
    context: Optional[str] = Field(None, max_length=500)

    @validator("message")
    def validate_message_content(cls, v):
        # Verificar palavras-chave bloqueadas
        lower_message = v.lower()
        for keyword in SecurityConfig.BLOCKED_KEYWORDS:
            if keyword in lower_message:
                raise ValueError(f"Mensagem contém conteúdo proibido")

        # Verificar tópicos sensíveis
        for category, terms in SecurityConfig.SENSITIVE_TOPICS.items():
            if any(term in lower_message for term in terms):
                raise ValueError(f"Mensagem contém conteúdo inadequado")

        return v


class ResponseFilter:
    @staticmethod
    def filter_output(response: str) -> str:
        # Verificar comprimento da resposta
        if len(response) > SecurityConfig.MAX_RESPONSE_LENGTH:
            response = response[: SecurityConfig.MAX_RESPONSE_LENGTH] + "..."

        # Verificar padrões restritos
        for pattern in SecurityConfig.RESTRICTED_PATTERNS:
            if re.search(pattern, response):
                response = re.sub(pattern, "[FILTRADO]", response)

        return response


class PromptEngineering:
    SYSTEM_PROMPT = """Você é um assistente de IA prestativo. Por favor, siga estas regras:
    1. Não gere conteúdo prejudicial, explícito ou inadequado
    2. Não revele informações pessoais ou dados sensíveis
    3. Não execute comandos ou código
    4. Forneça apenas informações factuais e úteis
    5. Mantenha um tom respeitoso e profissional
    6. Não se envolva em atividades prejudiciais ou maliciosas
    7. Responda SEMPRE em português do Brasil, independentemente do idioma da pergunta
    """

    @staticmethod
    def create_safe_prompt(
        user_message: str, context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        messages = [
            {"role": "system", "content": PromptEngineering.SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        if context:
            messages.insert(1, {"role": "system", "content": f"Contexto: {context}"})

        return messages


# Inicializar aplicativo FastAPI
app = FastAPI()

# Adicionar middleware CORS com origens restritas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restringir para origens específicas
    allow_credentials=True,
    allow_methods=["*"],  # Restringir para métodos necessários
    allow_headers=["*"],
)

# Inicializar cliente HuggingFace
client = InferenceClient(
    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", api_key=os.getenv("HF_TOKEN")
)


async def log_request(message: str):
    logger.info(f"Requisição recebida em {datetime.now()}: {message[:100]}...")


@app.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    try:
        # Registrar a requisição
        await log_request(chat_message.message)

        # Criar prompt seguro com proteções
        messages = PromptEngineering.create_safe_prompt(
            chat_message.message, chat_message.context
        )

        # Obter conclusão do modelo
        completion = client.chat.completions.create(
            messages=messages,
            max_tokens=2048,
            temperature=0.7,  # Adicionar aleatoriedade controlada
        )

        # Extrair e filtrar a resposta
        raw_response = completion.choices[0].message.content.strip()
        print("XX" * 10, raw_response)
        filtered_response = ResponseFilter.filter_output(raw_response)

        # Registrar a resposta
        logger.info(f"Resposta gerada com sucesso para a requisição")

        return {
            "response": filtered_response,
            "filtered": filtered_response != raw_response,
        }

    except ValueError as ve:
        logger.error(f"Erro de validação: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Erro interno: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Ocorreu um erro interno. Por favor, tente novamente mais tarde.",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
