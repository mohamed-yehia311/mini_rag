from ..LLM_Interface import LLM_interface
from models.enums import OpenAIEnums
from openai import OpenAI
import logging
import requests
from huggingface_hub import InferenceClient

class OpenAiProvider(LLM_interface):
    def __init__(self, api_key: str, api_url: str=None,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
            
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key = self.api_key,
            base_url = self.api_url if self.api_url and len(self.api_url) else None
        )

        self.enums = OpenAIEnums
        self.logger = logging.getLogger(__name__)
        
    def set_generating_model(self, model_id):
        self.generation_model_id = model_id
        
    def set_embedding_model(self, model_id, embedding_size):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    
    def construct_prompt(self, prompt, role):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }        
        
    def generate_text(self, prompt, chat_history, max_output_tokens = None, temperature = None):
        
        if not self.client:
            self.logger.error("Opne ai client wasn't set") 
            return None
        
        if  not self.generation_model_id:
            self.logger.error("generation model id wasn't set")
            return None
    
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature
        
        chat_history.append(
            self.construct_prompt(prompt=prompt, role= OpenAIEnums.USER.value)
        )       
        
        response = self.client.chat.completions.create(
            model = self.generation_model_id,
            messages = chat_history,
            max_tokens = max_output_tokens,
            temperature = temperature
        )
        
        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None
            
        return response.choices[0].message

   
    def generate_embedding(self, text, document_type=None):

        client = InferenceClient(
        provider="hf-inference",
        api_key=self.api_key,
        )

        result = client.feature_extraction(
            text,
            model=self.embedding_model_id,
        )

        return result.tolist()


    # def generate_embedding(self, text, document_type = None):
        
    #     if not self.client:
    #         self.logger.error("Opne ai client wasn't set") 
    #         return None
        
    #     if not self.embedding_model_id:
    #         self.logger.error("embbedding model id wasn't set") 
    #         return None

    #     response = self.client.embeddings.create(
    #         model = self.embedding_model_id,
    #         input = text,
    #     )
        
    #     if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
    #         self.logger.error("Error while generating Embedding with OpenAi")
    #         return None
            
    #     return response.data[0].embedding