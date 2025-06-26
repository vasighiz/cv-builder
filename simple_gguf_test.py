"""
Simple GGUF Test
Purpose: Quick test of GGUF functionality
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_basic_imports():
    """Test basic imports"""
    print("🧪 Testing imports...")
    
    try:
        from ctransformers import AutoModelForCausalLM
        print("✅ ctransformers imported")
    except ImportError as e:
        print(f"❌ ctransformers import failed: {e}")
        return False
    
    try:
        from src.modules.local_llm_manager import GGUFProvider, MISTRAL_7B_GGUF_CONFIG
        print("✅ GGUF modules imported")
    except ImportError as e:
        print(f"❌ GGUF modules import failed: {e}")
        return False
    
    return True

def test_model_loading():
    """Test model loading"""
    print("\n🔄 Testing model loading...")
    
    try:
        from src.modules.local_llm_manager import GGUFProvider, MISTRAL_7B_GGUF_CONFIG
        
        print("   Loading GGUF model (this may take a moment)...")
        provider = GGUFProvider(MISTRAL_7B_GGUF_CONFIG)
        
        if provider.is_available():
            print("✅ Model loaded successfully")
            return True
        else:
            print("❌ Model not available")
            return False
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def test_simple_generation():
    """Test simple text generation"""
    print("\n💬 Testing text generation...")
    
    try:
        from src.modules.local_llm_manager import create_llm_manager
        
        manager = create_llm_manager()
        
        test_prompt = "Hello, how are you?"
        print(f"   Generating response for: '{test_prompt}'")
        
        response = manager.generate(test_prompt, max_tokens=50)
        
        if "Error" not in response:
            print("✅ Generation successful")
            print(f"   Response: {response}")
            return True
        else:
            print(f"❌ Generation failed: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error in generation: {e}")
        return False

def main():
    """Run tests"""
    print("🚀 Simple GGUF Test")
    print("=" * 40)
    
    tests = [
        ("Imports", test_basic_imports),
        ("Model Loading", test_model_loading),
        ("Text Generation", test_simple_generation)
    ]
    
    for test_name, test_func in tests:
        if not test_func():
            print(f"\n❌ Test '{test_name}' failed")
            return False
    
    print("\n🎉 All tests passed! GGUF is working.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 