import os
from abc import ABC, abstractmethod
from typing import Any, Union, List
from openai import OpenAI
from google.genai import types
from google import genai
from messages import Message

class BaseLLM(ABC):

    @abstractmethod
    def generate(
        self, 
        prompt: str,
        *kwargs: Any
    ) -> Any: #Fix the output validation type once finished the validation!
        pass

    @abstractmethod
    def chat(
        self, 
        messages: List[Message],
        *kwargs: Any
    ) -> Any: #Fix the output validation type once finished the validation!
        pass

    @abstractmethod
    def __call__(
        self, 
        input: Union[str, List[Message]],
        *kwargs: Any
    ) -> Any: #Fix the output validation type once finished the validation!
        pass

class OpenAIModel(BaseLLM):

    def __init__(
            self,
            model: str = "gpt-4o-2024-05-13",
            api_key: str | None = None,  
            max_tokens: int = 4096,
            temperature: int = 0.6
    ):
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")

        self.client = OpenAI(api_key=api_key)
        
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def generate(
            self, 
            prompt: str
    ) -> str: #Fix the output validation type once finished the validation!
            
        message = [
            {"role": "user", "content": [
                  {"type": "text", "text": prompt}
            ]}
        ]
        completion = self.client.chat.completions.create(
            model = self.model,
            messages = message,
            max_tokens = self.max_tokens,
            temperature = self.temperature
        )
        return completion.choices[0].message
    
    def chat(
            self, 
            messages: List[Message]
    ) -> str: #Fix the output validation type once finished the validation!
        try:
            completion = self.client.chat.completions.create(
            model = self.model,
            messages = messages,   
            max_tokens = self.max_tokens,
            temperature = self.temperature
        )
            return completion.choices[0].message
        except Exception as e:
            print(f"Error while making request {e}")
    
    def __call__(self, 
                 input: Union[str, List[Message]]
    ) -> str: #Fix the output validation type once finished the validation!
        if isinstance(input, str):
            output = self.generate(prompt=str)
        else:
            output = self.chat(messages=input)
        return output

class GoogleAIModel(BaseLLM):
    def __init__(
            self, 
            model: str = "gemini-2.0-flash",
            api_key: str | None = None,
            max_tokens: int = 4096,
            temperature: int = 0.6,
            top_p: int = 0.5
    ):
        if not api_key:
            api_key = os.getenv("GENAI_API_KEY")

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self._config = self.create_config()
    
    def create_config(self) -> types.GenerateContentConfig:
        """Create a configuration for Google AI Model."""
        return types.GenerateContentConfig(
                max_output_tokens=self.max_tokens,
                temperature=self.temperature
                )
    @property
    def config(self) -> types.GenerateContentConfig:
        """Get the current configuration."""
        return self._config

    @config.setter
    def config(self, new_config: types.GenerateContentConfig) -> None:
        """Set a new configuration."""
        self._config = new_config

    def generate(self, 
                 prompt: str) -> str:
        try:
            completion = self.client.models.generate_content(
            model=self.model,
            contents = [prompt],
            config=self._config
        )
            return completion.text
        except Exception as e:
            print(f"Error while making request: {e}")
    
    def chat(self,
             messages: List[Message]) -> str:
        try:
            chat_content = []
            system_instruction = None
            for message in messages:
                if message["role"] == "system":
                    system_instruction = message["content"]
                if message["role"] == "user":
                    chat_content.append(message["content"])
            if system_instruction:
                self._config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p
                )
            chat = self.client.chats.create(
                model=self.model,
                config=self.config
            )
            response = None
            for user_message in chat_content:
                response = chat.send_message(user_message)
            return response.text if response else ""
        except Exception as e:
            print(f"Error while making request: {e}")

                    
    def __call__(self, 
                 input: Union[str, List[Message]]) -> Message:
        if isinstance(input, str):
            return self.generate(prompt=str)
        elif isinstance(input, List):
            return self.chat(messages=input)
        else:
            print(f"Input must be a string or list of Message")