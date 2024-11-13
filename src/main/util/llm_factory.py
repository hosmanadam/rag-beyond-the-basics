import logging
from functools import cache
from os import environ, getenv
from typing import Optional

from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, ChatOpenAI, OpenAIEmbeddings
from langchain_openai.chat_models.base import BaseChatOpenAI

_logger = logging.getLogger(__name__)


@cache
def is_azure_openai_configured():
    return getenv("AZURE_OPENAI_ENDPOINT") and getenv("AZURE_OPENAI_API_KEY")


@cache
def is_openai_configured():
    return getenv("OPENAI_API_VERSION") and getenv("OPENAI_API_KEY")


def raise_not_configured():
    raise ValueError("OpenAI is not configured, please make sure you have the necessary variables in .env.")


@cache
def get_embedding_model() -> OpenAIEmbeddings:
    """Returns Azure OpenAI embedding model if available, else returns public OpenAI chat model."""
    model = environ["EMBEDDING_MODEL"]
    if is_azure_openai_configured():
        return AzureOpenAIEmbeddings(model=model)
    elif is_openai_configured():
        return OpenAIEmbeddings(model=model)
    else:
        raise_not_configured()


@cache
def get_chat_model() -> BaseChatOpenAI:
    """Returns Azure OpenAI chat model if available, else returns public OpenAI chat model."""
    model = environ["CHAT_MODEL"]
    temperature = float(environ["CHAT_MODEL_TEMPERATURE"])
    top_p = float(environ["CHAT_MODEL_TOP_P"])
    if is_azure_openai_configured():
        return AzureChatOpenAI(deployment_name=model, temperature=temperature, top_p=top_p)
    elif is_openai_configured():
        return ChatOpenAI(model=model, temperature=temperature, top_p=top_p)
    else:
        raise_not_configured()


@cache
def get_evaluation_model() -> DeepEvalBaseLLM | str:
    """Returns DeepEval-ified Azure OpenAI chat model if available, else returns public OpenAI chat model."""
    model = environ["EVALUATION_MODEL"]
    temperature = float(environ["EVALUATION_MODEL_TEMPERATURE"])
    top_p = float(environ["EVALUATION_MODEL_TOP_P"])

    if is_openai_configured():
        _logger.warning("Using OpenAI evaluation model!")
        return model
    elif is_azure_openai_configured():
        _logger.warning("Evaluation model will probably not work with custom model!")
        return CustomEvaluationModel(AzureChatOpenAI(deployment_name=model, temperature=temperature, top_p=top_p))
    else:
        raise_not_configured()

    # FIXME: ValueError: Evaluation LLM outputted an invalid JSON. Please use a better evaluation model.
    # if is_azure_openai_configured():
    #     return CustomEvaluationModel(AzureChatOpenAI(deployment_name=model, temperature=temperature, top_p=top_p))
    # elif is_openai_configured():
    #     return CustomEvaluationModel(ChatOpenAI(model=model, temperature=temperature, top_p=top_p))
    # else:
    #     raise_not_configured()


class CustomEvaluationModel(DeepEvalBaseLLM):
    def __init__(self, model):
        self.model = model

    def load_model(self):
        return self.model

    def set_config(self, config: Optional[RunnableConfig] = None) -> None:
        if config:
            self.model = self.model.with_config(config)

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        return chat_model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        res = await chat_model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return self.model.get_name()
