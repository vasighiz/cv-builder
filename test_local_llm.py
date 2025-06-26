"""
Test script for Local LLM functionality
Purpose: Test the local LLM manager and interface
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from modules.llm_interface import LLMInterface, create_llm_interface
from modules.local_llm_manager import LLMManager, MISTRAL_7B_CONFIG, GPT4_CONFIG

def test_llm_manager():
    """Test the LLM manager directly"""
    print("🧪 Testing LLM Manager")
    print("=" * 50)
    
    manager = LLMManager()
    
    # Test available models
    print("📋 Available models:")
    models = manager.get_available_models()
    for provider, model_list in models.items():
        print(f"{provider.capitalize()}: {', '.join(model_list[:3])}...")
    
    # Test connections
    print("\n🔗 Testing connections:")
    local_available = manager.test_connection("local")
    api_available = manager.test_connection("api")
    
    print(f"Local: {'✅ Available' if local_available else '❌ Not available'}")
    print(f"API: {'✅ Available' if api_available else '❌ Not available'}")
    
    return local_available, api_available

def test_local_generation():
    """Test local model generation"""
    print("\n🚀 Testing Local Model Generation")
    print("=" * 50)
    
    llm = create_llm_interface("local")
    
    # Test simple prompt
    test_prompt = "Write a one-sentence professional summary for a software engineer."
    
    print(f"Prompt: {test_prompt}")
    print("Generating response...")
    
    response = llm.generate_response(test_prompt)
    
    if response:
        print(f"✅ Response: {response}")
    else:
        print("❌ No response generated")
    
    return response

def test_provider_switching():
    """Test switching between providers"""
    print("\n🔄 Testing Provider Switching")
    print("=" * 50)
    
    llm = create_llm_interface("local")
    
    # Test switching to API
    print("Switching to API provider...")
    success = llm.set_provider("api")
    print(f"Switch result: {'✅ Success' if success else '❌ Failed'}")
    
    # Test switching back to local
    print("Switching back to local provider...")
    success = llm.set_provider("local")
    print(f"Switch result: {'✅ Success' if success else '❌ Failed'}")
    
    return success

def test_usage_stats():
    """Test usage statistics tracking"""
    print("\n📊 Testing Usage Statistics")
    print("=" * 50)
    
    llm = create_llm_interface("local")
    
    # Generate a few responses
    prompts = [
        "Write a brief professional summary.",
        "List 3 key skills for a data scientist.",
        "Describe a project achievement."
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"Generating response {i}...")
        response = llm.generate_response(prompt)
        if response:
            print(f"✅ Response {i}: {response[:50]}...")
        else:
            print(f"❌ No response for prompt {i}")
    
    # Show stats
    stats = llm.get_usage_stats()
    print("\n📈 Usage Statistics:")
    for provider, data in stats.items():
        print(f"{provider.capitalize()}: {data['calls']} calls, {data['tokens']} tokens, {data['errors']} errors")

def test_error_handling():
    """Test error handling"""
    print("\n⚠️ Testing Error Handling")
    print("=" * 50)
    
    llm = create_llm_interface("local")
    
    # Test with empty prompt
    print("Testing empty prompt...")
    response = llm.generate_response("")
    print(f"Empty prompt response: {'✅ Generated' if response else '❌ No response'}")
    
    # Test with very long prompt
    print("Testing very long prompt...")
    long_prompt = "Test " * 1000
    response = llm.generate_response(long_prompt)
    print(f"Long prompt response: {'✅ Generated' if response else '❌ No response'}")

def main():
    """Main test function"""
    print("🎯 Local LLM Test Suite")
    print("=" * 60)
    
    try:
        # Test LLM manager
        local_available, api_available = test_llm_manager()
        
        if local_available:
            # Test local generation
            test_local_generation()
            
            # Test provider switching
            test_provider_switching()
            
            # Test usage stats
            test_usage_stats()
            
            # Test error handling
            test_error_handling()
            
            print("\n🎉 All tests completed successfully!")
        else:
            print("\n❌ Local LLM not available. Please check your setup.")
            print("Make sure you have:")
            print("- PyTorch installed")
            print("- Transformers library installed")
            print("- Sufficient disk space for model download")
            print("- Sufficient RAM/VRAM for model loading")
        
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 