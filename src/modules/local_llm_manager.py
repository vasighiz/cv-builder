"""
Local LLM Manager Module
Purpose: Manage local LLM models (Mistral 7B GGUF, etc.) with easy switching between local and API models
"""

import os
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
import torch
from dotenv import load_dotenv

# Import ctransformers for GGUF support
try:
    from ctransformers import AutoModelForCausalLM, AutoTokenizer
    CTTRANSFORMERS_AVAILABLE = True
except ImportError:
    CTTRANSFORMERS_AVAILABLE = False
    print("⚠️  ctransformers not available. Install with: pip install ctransformers")

# Import OpenAI for API fallback
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI not available. Install with: pip install openai")

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
    model_path: Optional[str] = None
    max_length: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    repetition_penalty: float = 1.1
    context_length: int = 4096
    gpu_layers: int = 0  # 0 for CPU, >0 for GPU layers
    threads: int = 4

# Predefined configurations
MISTRAL_7B_GGUF_CONFIG = LLMConfig(
    model_name="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    model_type="local",
    model_path="./models/mistralai/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    max_length=2048,
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    repetition_penalty=1.1,
    context_length=4096,
    gpu_layers=35,  # Use GPU for most layers on GTX 1660 Ti
    threads=4
)

GPT4_CONFIG = LLMConfig(
    model_name="gpt-4o",
    model_type="api",
    max_length=2048,
    temperature=0.7
)

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available"""
        pass

class GGUFProvider(BaseLLMProvider):
    """GGUF model provider using ctransformers"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load GGUF model"""
        if not CTTRANSFORMERS_AVAILABLE:
            raise ImportError("ctransformers not available")
        
        model_path = self.config.model_path
        if not model_path or not Path(model_path).exists():
            raise FileNotFoundError(f"Model not found at: {model_path}")
        
        try:
            logger.info(f"🔄 Loading GGUF model: {model_path}")
            
            # Load model with GPU acceleration if available
            model_kwargs = {
                "model_type": "mistral",  # or auto-detect
                "gpu_layers": self.config.gpu_layers,
                "threads": self.config.threads,
                "context_length": self.config.context_length,
                "max_new_tokens": self.config.max_length,
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
                "top_k": self.config.top_k,
                "repetition_penalty": self.config.repetition_penalty
            }
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                **model_kwargs
            )
            
            logger.info(f"✅ GGUF model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Error loading GGUF model: {e}")
            raise
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using GGUF model"""
        if not self.model:
            raise RuntimeError("Model not loaded")
        
        try:
            # Prepare prompt with Mistral format
            formatted_prompt = f"<s>[INST] {prompt} [/INST]"
            
            # Generate response
            response = self.model(
                formatted_prompt,
                max_new_tokens=kwargs.get('max_tokens', self.config.max_length),
                temperature=kwargs.get('temperature', self.config.temperature),
                top_p=kwargs.get('top_p', self.config.top_p),
                top_k=kwargs.get('top_k', self.config.top_k),
                repetition_penalty=kwargs.get('repetition_penalty', self.config.repetition_penalty),
                stop=["</s>", "[INST]"]  # Stop at end tokens
            )
            
            # Clean up response
            if isinstance(response, list):
                response = response[0]
            
            # Remove the prompt from response
            if formatted_prompt in response:
                response = response.replace(formatted_prompt, "").strip()
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error generating text: {e}")
            return f"Error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if GGUF provider is available"""
        return CTTRANSFORMERS_AVAILABLE and self.model is not None

class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize OpenAI client"""
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI not available")
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        self.client = OpenAI(api_key=api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using OpenAI API"""
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get('max_tokens', self.config.max_length),
                temperature=kwargs.get('temperature', self.config.temperature),
                top_p=kwargs.get('top_p', self.config.top_p)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"❌ Error generating text with OpenAI: {e}")
            return f"Error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if OpenAI provider is available"""
        return OPENAI_AVAILABLE and self.client is not None

class LLMManager:
    """Manager for multiple LLM providers"""
    
    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.current_provider = "local"
        self.usage_stats = {
            "local": {"calls": 0, "total_tokens": 0, "errors": 0},
            "api": {"calls": 0, "total_tokens": 0, "errors": 0}
        }
    
    def add_provider(self, name: str, provider: BaseLLMProvider):
        """Add a provider"""
        self.providers[name] = provider
        logger.info(f"✅ Added provider: {name}")
    
    def set_provider(self, name: str):
        """Set current provider"""
        if name in self.providers:
            self.current_provider = name
            logger.info(f"🔄 Switched to provider: {name}")
        else:
            raise ValueError(f"Provider not found: {name}")
    
    def get_provider(self, name: Optional[str] = None) -> BaseLLMProvider:
        """Get provider by name or current provider"""
        provider_name = name or self.current_provider
        if provider_name not in self.providers:
            raise ValueError(f"Provider not found: {provider_name}")
        return self.providers[provider_name]
    
    def generate(self, prompt: str, provider: Optional[str] = None, **kwargs) -> str:
        """Generate text using specified or current provider"""
        try:
            provider_name = provider or self.current_provider
            llm_provider = self.get_provider(provider_name)
            
            if not llm_provider.is_available():
                raise RuntimeError(f"Provider {provider_name} is not available")
            
            # Track usage
            self.usage_stats[provider_name]["calls"] += 1
            
            # Generate response
            start_time = time.time()
            response = llm_provider.generate(prompt, **kwargs)
            end_time = time.time()
            
            # Update stats
            self.usage_stats[provider_name]["total_tokens"] += len(response.split())
            
            logger.info(f"✅ Generated response in {end_time - start_time:.2f}s using {provider_name}")
            return response
            
        except Exception as e:
            provider_name = provider or self.current_provider
            self.usage_stats[provider_name]["errors"] += 1
            logger.error(f"❌ Error generating text: {e}")
            return f"Error: {str(e)}"
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get list of available models by provider"""
        models = {}
        for name, provider in self.providers.items():
            if provider.is_available():
                if isinstance(provider, GGUFProvider):
                    models[name] = [provider.config.model_name]
                elif isinstance(provider, OpenAIProvider):
                    models[name] = [provider.config.model_name]
        return models
    
    def get_usage_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get usage statistics"""
        return self.usage_stats.copy()
    
    def test_connections(self) -> Dict[str, bool]:
        """Test all provider connections"""
        results = {}
        for name, provider in self.providers.items():
            try:
                # Test with a simple prompt
                response = provider.generate("Hello, how are you?", max_tokens=10)
                results[name] = "Error" not in response
            except Exception as e:
                results[name] = False
                logger.error(f"❌ Connection test failed for {name}: {e}")
        return results

# Convenience functions
def create_llm_manager() -> LLMManager:
    """Create and configure LLM manager with default providers"""
    manager = LLMManager()
    
    # Add GGUF provider if model exists
    if CTTRANSFORMERS_AVAILABLE:
        try:
            gguf_provider = GGUFProvider(MISTRAL_7B_GGUF_CONFIG)
            manager.add_provider("local", gguf_provider)
            logger.info("✅ GGUF provider added")
        except Exception as e:
            logger.warning(f"⚠️  Could not add GGUF provider: {e}")
    
    # Add OpenAI provider if API key is available
    if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
        try:
            openai_provider = OpenAIProvider(GPT4_CONFIG)
            manager.add_provider("api", openai_provider)
            logger.info("✅ OpenAI provider added")
        except Exception as e:
            logger.warning(f"⚠️  Could not add OpenAI provider: {e}")
    
    return manager

def create_llm_interface(provider: str = "local") -> LLMManager:
    """Create LLM interface with specified provider"""
    manager = create_llm_manager()
    
    # Set default provider
    if provider in manager.providers:
        manager.set_provider(provider)
    else:
        available = list(manager.providers.keys())
        if available:
            manager.set_provider(available[0])
            logger.warning(f"⚠️  Provider '{provider}' not available, using '{available[0]}'")
        else:
            raise RuntimeError("No LLM providers available")
    
    return manager 