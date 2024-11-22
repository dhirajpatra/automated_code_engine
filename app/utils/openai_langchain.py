# app/utils/openai_langchain.py
import os
from logger import logger
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")
ORGANIZATION_NAME = os.getenv("ORGANIZATION_NAME")

def create_chain(prompt: str) -> LLMChain:
    """
    Creates an LLM chain using OpenAI model with the given prompt.
    """
    try:
        logger.info("Initializing OpenAI Chat model.")
        chat_model = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=OPENAI_API_KEY,
            organization=ORGANIZATION_ID,
            temperature=0.7,
            max_tokens=5000,
        )

        # Use a prompt template with the correct parameters
        # Since the prompt is static, no input_variables are required
        prompt_template = PromptTemplate(template=prompt, input_variables=[])

        # Log the prompt template for debugging
        logger.info(f"\n\nPrompt Template Created: {prompt_template}\n\n")

        # Create the LLM chain with the prompt
        return LLMChain(llm=chat_model, prompt=prompt_template)

    except Exception as e:
        logger.error(f"Error creating chain: {str(e)}")
        return None



async def generate_code(prompt: str) -> str:
    """
    Uses OpenAI API to generate code based on the input prompt.
    Returns a dictionary where keys are filenames and values are the code content.
    """
    try:
        logger.info(f"Generating code with prompt.")
        chain = create_chain(prompt)
        if chain is None:
            return {"error": "Error creating chain."}

        # Run the chain using ainvoke with an empty input as required
        response = await chain.ainvoke({})  # Pass an empty dictionary since no input variables are required

        # Log the response structure for debugging
        logger.info(f"\n\nResponse from OpenAI: {response}\n\n")

        return response

    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        return {"error": f"Error generating code: {str(e)}"}



