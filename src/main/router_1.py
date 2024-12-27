"""Route between general_1 and book_1 - book_3"""

import logging

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough

from src.main.book_1 import create_chain as create_book_chain
from src.main.general_1 import create_chain as create_general_chain
from src.main.util.llm_factory import get_chat_model

_logger = logging.getLogger(__name__)


def create_chain() -> Runnable:
    general_chain = create_general_chain()
    book_chain = create_book_chain()

    classification_prompt = """
    Given the user question below, classify it as either being about `book`, or `other`.
    
    Do not respond with more than one word.
    
    Here is an overview of the book:
    
    <overview>
    Author: C. O'Brien
    Title: Frank Hardy's Choice and What Came of It
    
    The story follows two young apprentices, Frank Hardy and Walter White, in the seaside village of Springcliffe. 
    Frank is disinterested in education and prefers to spend his free time with bad company, particularly Tom Haines, 
    while Walter is eager to improve himself by attending evening school. The narrative explores themes of choice, 
    consequence, and moral integrity.
    
    As the story unfolds, Frank succumbs to the influence of Tom Haines and becomes involved in poaching, leading to his 
    arrest and imprisonment. Meanwhile, Walter thrives through his education and hard work, eventually becoming a successful 
    builder and architect. The contrast between their paths highlights the impact of choices on their lives.
    
    Other characters include Mrs. White, Walter's supportive mother; Gracie Hardy, Frank's blind sister; and John Hardy, 
    Frank's irresponsible father. The story culminates in Frank's realization of his mistakes and his desire to change, 
    while Walter's life flourishes as he remains steadfast in his values. Ultimately, the book serves as a moral tale about 
    the importance of making wise choices and the consequences of one's actions.
    </overview>
    
    <question>
    {question}
    </question>
    
    Classification:"""

    router_chain = PromptTemplate.from_template(classification_prompt) | get_chat_model() | StrOutputParser()

    def route(info):
        if "book" in info["topic"].lower():
            _logger.info("Routing to book chain")
            return book_chain.invoke(info["question"])
        else:
            _logger.info("Routing to general chain")
            return general_chain.invoke(info["question"])

    return {"topic": router_chain, "question": RunnablePassthrough()} | RunnableLambda(route)


def run():
    _logger.info("Running app...")
    rag_chain = create_chain()
    while True:
        question = input("Your question (or 'q' to quit): ")
        if question.strip() == "q":
            print("Bye!")
            break
        else:
            response = rag_chain.invoke(question)
            print(f"Assistant: {response}")


if __name__ == "__main__":
    load_dotenv()
    run()
