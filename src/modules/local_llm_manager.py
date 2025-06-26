"""
Local LLM Manager Module
Purpose: Manage local LLM models (Mistral 7B, etc.) with easy switching between local and API models
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LLMConfig:
    """Configuration for LLM models"""
    model_name: str
    model_type: str  # 'local' or 'api'
    max_length: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    device: str = "auto"  # 'auto', 'cpu', 'cuda', 'mps'

@dataclass
class LLMResponse:
    """Standardized response format for LLM outputs"""
    content: str
    model_name: str
    model_type: str
    tokens_used: Optional[int] = None
    response_time: Optional[float] = None
    error: Optional[str] = None

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, config: LLMConfig) -> LLMResponse:
        """Generate response from LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available"""
        pass

class LocalLLMProvider(BaseLLMProvider):
    """Local LLM provider using Hugging Face models"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.device = self._get_device()
        
    def _get_device(self) -> str:
        """Determine the best available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def load_model(self, model_name: str, config: LLMConfig) -> bool:
        """Load the specified model"""
        try:
            logger.info(f"Loading local model: {model_name}")
            
            # Set device
            device = config.device if config.device != "auto" else self.device
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True,
                cache_dir="./models"
            )
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map=device if device != "cpu" else None,
                trust_remote_code=True,
                cache_dir="./models",
                low_cpu_mem_usage=True
            )
            
            # Create pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=device if device != "cpu" else -1,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            )
            
            logger.info(f"Model {model_name} loaded successfully on {device}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            return False
    
    def generate(self, prompt: str, config: LLMConfig) -> LLMResponse:
        """Generate response using local model"""
        try:
            if self.pipeline is None:
                if not self.load_model(config.model_name, config):
                    return LLMResponse(
                        content="",
                        model_name=config.model_name,
                        model_type="local",
                        error="Failed to load model"
                    )
            
            # Generate response
            response = self.pipeline(
                prompt,
                max_length=config.max_length,
                temperature=config.temperature,
                top_p=config.top_p,
                top_k=config.top_k,
                repetition_penalty=config.repetition_penalty,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                return_full_text=False
            )
            
            # Extract generated text
            generated_text = response[0]['generated_text'] if response else ""
            
            return LLMResponse(
                content=generated_text.strip(),
                model_name=config.model_name,
                model_type="local",
                tokens_used=len(self.tokenizer.encode(generated_text))
            )
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return LLMResponse(
                content="",
                model_name=config.model_name,
                model_type="local",
                error=str(e)
            )
    
    def is_available(self) -> bool:
        """Check if local model is available"""
        return self.pipeline is not None

class APILLMProvider(BaseLLMProvider):
    """API LLM provider (OpenAI, etc.)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self._available = True
        except ImportError:
            logger.error("OpenAI library not installed")
            self._available = False
    
    def generate(self, prompt: str, config: LLMConfig) -> LLMResponse:
        """Generate response using API"""
        try:
            if not self._available:
                return LLMResponse(
                    content="",
                    model_name=config.model_name,
                    model_type="api",
                    error="API provider not available"
                )
            
            response = self.client.chat.completions.create(
                model=config.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=config.max_length,
                temperature=config.temperature,
                top_p=config.top_p,
                frequency_penalty=config.repetition_penalty - 1.0
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model_name=config.model_name,
                model_type="api",
                tokens_used=response.usage.total_tokens
            )
            
        except Exception as e:
            logger.error(f"Error generating API response: {e}")
            return LLMResponse(
                content="",
                model_name=config.model_name,
                model_type="api",
                error=str(e)
            )
    
    def is_available(self) -> bool:
        """Check if API provider is available"""
        return self._available

class LLMManager:
    """Main LLM manager for switching between local and API models"""
    
    def __init__(self, default_config: Optional[LLMConfig] = None):
        self.default_config = default_config or LLMConfig(
            model_name="mistralai/Mistral-7B-Instruct-v0.2",
            model_type="local"
        )
        self.local_provider = LocalLLMProvider()
        self.api_provider = None
        self.current_provider = None
        
        # Initialize API provider if key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.api_provider = APILLMProvider(api_key)
    
    def set_provider(self, provider_type: str) -> bool:
        """Set the current LLM provider"""
        if provider_type == "local":
            self.current_provider = self.local_provider
            return True
        elif provider_type == "api" and self.api_provider:
            self.current_provider = self.api_provider
            return True
        else:
            logger.error(f"Provider type '{provider_type}' not available")
            return False
    
    def generate(self, prompt: str, config: Optional[LLMConfig] = None) -> LLMResponse:
        """Generate response using current provider"""
        if config is None:
            config = self.default_config
        
        if self.current_provider is None:
            # Auto-select provider based on config
            if config.model_type == "local":
                self.current_provider = self.local_provider
            elif config.model_type == "api" and self.api_provider:
                self.current_provider = self.api_provider
            else:
                return LLMResponse(
                    content="",
                    model_name=config.model_name,
                    model_type=config.model_type,
                    error="No suitable provider available"
                )
        
        return self.current_provider.generate(prompt, config)
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get list of available models"""
        models = {
            "local": [
                "mistralai/Mistral-7B-Instruct-v0.2",
                "microsoft/DialoGPT-medium",
                "gpt2",
                "EleutherAI/gpt-neo-125M"
            ],
            "api": [
                "gpt-4",
                "gpt-3.5-turbo",
                "gpt-4o"
            ]
        }
        return models
    
    def test_connection(self, provider_type: str) -> bool:
        """Test connection to specified provider"""
        if provider_type == "local":
            return self.local_provider.is_available()
        elif provider_type == "api":
            return self.api_provider.is_available() if self.api_provider else False
        return False

# Predefined configurations for common models
MISTRAL_7B_CONFIG = LLMConfig(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    model_type="local",
    max_length=2048,
    temperature=0.7,
    top_p=0.9,
    top_k=50,
    repetition_penalty=1.1
)

GPT4_CONFIG = LLMConfig(
    model_name="gpt-4",
    model_type="api",
    max_length=2048,
    temperature=0.7,
    top_p=0.9,
    top_k=50,
    repetition_penalty=1.1
)

# Usage example and testing functions
def test_local_llm():
    """Test function for local LLM"""
    manager = LLMManager()
    
    # Test local model
    print("Testing local LLM...")
    manager.set_provider("local")
    
    test_prompt = "Write a brief professional summary for a data scientist resume."
    response = manager.generate(test_prompt, MISTRAL_7B_CONFIG)
    
    print(f"Response: {response.content}")
    print(f"Model: {response.model_name}")
    print(f"Type: {response.model_type}")
    print(f"Tokens: {response.tokens_used}")
    if response.error:
        print(f"Error: {response.error}")

def test_api_llm():
    """Test function for API LLM"""
    manager = LLMManager()
    
    # Test API model
    print("Testing API LLM...")
    if manager.set_provider("api"):
        test_prompt = "Write a brief professional summary for a data scientist resume."
        response = manager.generate(test_prompt, GPT4_CONFIG)
        
        print(f"Response: {response.content}")
        print(f"Model: {response.model_name}")
        print(f"Type: {response.model_type}")
        print(f"Tokens: {response.tokens_used}")
        if response.error:
            print(f"Error: {response.error}")
    else:
        print("API provider not available")

if __name__ == "__main__":
    # Run tests
    test_local_llm()
    print("\n" + "="*50 + "\n")
    test_api_llm() 