from abc  import ABC, abstractmethod

class LLM_interface(ABC):
 
     
    @abstractmethod
    def set_generating_model(self, model_id: str):
        pass
    
    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass
       
    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        pass
    
    @abstractmethod
    def generate_embedding(self, text: str, document_type: str = None):
        pass
    
    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass