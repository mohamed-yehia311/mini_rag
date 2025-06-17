import cohere
from models.enums import CoHereEnums
from ..LLM_Interface import LLM_interface
import logging


class CoherProvider(LLM_interface):
    
    def __init__(self, api_key: str,
                        default_input_max_characters: int=1000,
                        default_generation_max_output_tokens: int=1000,
                        default_generation_temperature: float=0.1):
            
            self.api_key = api_key

            self.default_input_max_characters = default_input_max_characters
            self.default_generation_max_output_tokens = default_generation_max_output_tokens
            self.default_generation_temperature = default_generation_temperature

            self.generation_model_id = None
            
            self.enums = CoHereEnums   
            
            self.embedding_model_id = None
            self.embedding_size = None

            self.client = cohere.Client(api_key=self.api_key)

            self.logger = logging.getLogger(__name__)
            
            
    def set_generating_model(self, model_id):
        self.generate_model_id = model_id
        
        
    def set_embedding_model(self, model_id, embedding_size):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    
    def construct_prompt(self, prompt, role):
        return{
            "role": role,
            "text": prompt
        }         
        
    def generate_text(self, prompt, chat_history = ..., max_output_tokens = None, temperature = None):
       
        if not self.client:
            self.logger.error("Coher Clien wasn't set")
            return None
        
        if not self.api_key:
            self.logger.error("Coher API wasn't set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if  temperature else self.default_generation_temperature
        
        response= self.client.chat(
            model = self.generation_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens            
        )
        
        if not response or not response.text:
            self.logger.error("Error while generating Text with Coher")
            return None
        
        return response.text
    
    def generate_embedding(self, text: str, document_type: str = None):
        
        if not self.client:
            self.logger.error("Coher Clien wasn't set")
            return None
        
        if not self.api_key:
            self.logger.error("Coher API wasn't set")
            return None
        
        response = self.client.embed(
            model = self.embedding_model_id,
            texts = [self.process_text(text)],
            input_type = document_type,
            embedding_types=['float'],
        )

        if not response or not response.embeddings or not response.embeddings.float_[0]:
            self.logger.error("Error while embedding text with CoHere")
            return None
        
        return response.embeddings.float_[0]            