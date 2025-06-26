"""
LLM Interface Module
Purpose: Unified interface for switching between local and API LLM models in resume builder modules
"""

import os
import time
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Import our LLM manager
from .local_llm_manager import LLMManager, LLMConfig, MISTRAL_7B_CONFIG, GPT4_CONFIG

# Load environment variables
load_dotenv()

class LLMInterface:
    """Unified interface for LLM operations in resume builder"""
    
    def __init__(self, default_provider: str = "local"):
        """
        Initialize LLM interface
        
        Args:
            default_provider (str): Default provider ('local' or 'api')
        """
        self.manager = LLMManager()
        self.default_provider = default_provider
        self.current_provider = default_provider
        
        # Set initial provider
        self.set_provider(default_provider)
        
        # Track usage statistics
        self.usage_stats = {
            "local": {"calls": 0, "tokens": 0, "errors": 0},
            "api": {"calls": 0, "tokens": 0, "errors": 0}
        }
    
    def set_provider(self, provider: str) -> bool:
        """
        Switch between local and API providers
        
        Args:
            provider (str): 'local' or 'api'
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.manager.set_provider(provider):
            self.current_provider = provider
            print(f"✅ Switched to {provider} LLM provider")
            return True
        else:
            print(f"❌ Failed to switch to {provider} provider")
            return False
    
    def generate_response(self, prompt: str, config: Optional[LLMConfig] = None) -> str:
        """
        Generate response using current provider
        
        Args:
            prompt (str): Input prompt
            config (LLMConfig): Optional configuration override
            
        Returns:
            str: Generated response
        """
        start_time = time.time()
        
        # Use default config if none provided
        if config is None:
            if self.current_provider == "local":
                config = MISTRAL_7B_CONFIG
            else:
                config = GPT4_CONFIG
        
        # Generate response
        response = self.manager.generate(prompt, config)
        
        # Update usage statistics
        self._update_stats(response, time.time() - start_time)
        
        if response.error:
            print(f"❌ LLM Error ({self.current_provider}): {response.error}")
            return ""
        
        return response.content
    
    def _update_stats(self, response, response_time: float):
        """Update usage statistics"""
        provider = response.model_type
        self.usage_stats[provider]["calls"] += 1
        
        if response.tokens_used:
            self.usage_stats[provider]["tokens"] += response.tokens_used
        
        if response.error:
            self.usage_stats[provider]["errors"] += 1
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return self.usage_stats.copy()
    
    def test_providers(self) -> Dict[str, bool]:
        """Test both local and API providers"""
        results = {}
        
        print("🧪 Testing LLM providers...")
        
        # Test local provider
        print("Testing local provider...")
        results["local"] = self.manager.test_connection("local")
        print(f"Local provider: {'✅ Available' if results['local'] else '❌ Not available'}")
        
        # Test API provider
        print("Testing API provider...")
        results["api"] = self.manager.test_connection("api")
        print(f"API provider: {'✅ Available' if results['api'] else '❌ Not available'}")
        
        return results
    
    def get_available_models(self) -> Dict[str, list]:
        """Get list of available models"""
        return self.manager.get_available_models()

# Convenience functions for resume builder modules
def create_llm_interface(provider: str = "local") -> LLMInterface:
    """
    Create LLM interface with specified provider
    
    Args:
        provider (str): 'local' or 'api'
        
    Returns:
        LLMInterface: Configured LLM interface
    """
    return LLMInterface(default_provider=provider)

def generate_resume_content(prompt: str, provider: str = "local") -> str:
    """
    Generate resume content using specified provider
    
    Args:
        prompt (str): Content generation prompt
        provider (str): 'local' or 'api'
        
    Returns:
        str: Generated content
    """
    llm = create_llm_interface(provider)
    return llm.generate_response(prompt)

# Example usage and testing
def test_llm_interface():
    """Test the LLM interface"""
    print("🚀 Testing LLM Interface")
    print("=" * 50)
    
    # Create interface
    llm = create_llm_interface("local")
    
    # Test providers
    results = llm.test_providers()
    
    # Test content generation
    test_prompt = """
    Create a professional summary for a data scientist resume with the following requirements:
    - 3-4 sentences maximum
    - Focus on machine learning and data analysis
    - Include Python and SQL skills
    - Professional tone
    """
    
    print("\n📝 Testing content generation...")
    response = llm.generate_response(test_prompt)
    
    if response:
        print("✅ Generated content:")
        print(response)
    else:
        print("❌ Failed to generate content")
    
    # Show usage stats
    print("\n📊 Usage Statistics:")
    stats = llm.get_usage_stats()
    for provider, data in stats.items():
        print(f"{provider.capitalize()}: {data['calls']} calls, {data['tokens']} tokens, {data['errors']} errors")

if __name__ == "__main__":
    test_llm_interface() 