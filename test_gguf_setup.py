"""
Test GGUF Setup
Purpose: Test the GGUF model setup and functionality
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_gguf_imports():
    """Test if GGUF dependencies are available"""
    print("🧪 Testing GGUF Dependencies")
    print("=" * 50)
    
    try:
        from ctransformers import AutoModelForCausalLM
        print("✅ ctransformers imported successfully")
    except ImportError as e:
        print(f"❌ ctransformers import failed: {e}")
        return False
    
    try:
        from src.modules.local_llm_manager import GGUFProvider, MISTRAL_7B_GGUF_CONFIG
        print("✅ GGUF modules imported successfully")
    except ImportError as e:
        print(f"❌ GGUF modules import failed: {e}")
        return False
    
    return True

def test_model_path():
    """Test if the GGUF model file exists"""
    print("\n📁 Testing Model Path")
    print("=" * 50)
    
    model_path = Path("./models/mistralai/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
    
    if model_path.exists():
        print(f"✅ Model found at: {model_path}")
        print(f"   Size: {model_path.stat().st_size / (1024**3):.2f} GB")
        return True
    else:
        print(f"❌ Model not found at: {model_path}")
        print("   Please ensure the GGUF model is in the correct location")
        return False

def test_gguf_provider():
    """Test GGUF provider initialization"""
    print("\n🔧 Testing GGUF Provider")
    print("=" * 50)
    
    try:
        from src.modules.local_llm_manager import GGUFProvider, MISTRAL_7B_GGUF_CONFIG
        
        print("🔄 Initializing GGUF provider...")
        provider = GGUFProvider(MISTRAL_7B_GGUF_CONFIG)
        
        if provider.is_available():
            print("✅ GGUF provider initialized successfully")
            return True
        else:
            print("❌ GGUF provider not available")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing GGUF provider: {e}")
        return False

def test_llm_manager():
    """Test LLM manager with GGUF"""
    print("\n🎛️  Testing LLM Manager")
    print("=" * 50)
    
    try:
        from src.modules.local_llm_manager import create_llm_manager
        
        print("🔄 Creating LLM manager...")
        manager = create_llm_manager()
        
        print(f"📋 Available providers: {list(manager.providers.keys())}")
        
        # Test connections
        connections = manager.test_connections()
        for provider, status in connections.items():
            print(f"   {provider}: {'✅ Available' if status else '❌ Not available'}")
        
        return any(connections.values())
        
    except Exception as e:
        print(f"❌ Error testing LLM manager: {e}")
        return False

def test_generation():
    """Test text generation with GGUF"""
    print("\n💬 Testing Text Generation")
    print("=" * 50)
    
    try:
        from src.modules.local_llm_manager import create_llm_manager
        
        manager = create_llm_manager()
        
        # Test with a simple prompt
        test_prompt = "Write a brief professional summary for a data scientist."
        
        print(f"🔄 Generating response for: '{test_prompt}'")
        print("   (This may take a few seconds for the first generation)")
        
        response = manager.generate(test_prompt, max_tokens=100)
        
        if "Error" not in response:
            print("✅ Text generation successful")
            print(f"📝 Response: {response[:200]}...")
            return True
        else:
            print(f"❌ Generation failed: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing generation: {e}")
        return False

def test_llm_interface():
    """Test the LLM interface"""
    print("\n🔌 Testing LLM Interface")
    print("=" * 50)
    
    try:
        from src.modules.llm_interface import create_llm_interface
        
        print("🔄 Creating LLM interface...")
        llm = create_llm_interface("local")
        
        # Test available providers
        providers = llm.get_available_providers()
        print(f"📋 Available providers: {providers}")
        
        # Test connection
        if llm.test_connection():
            print("✅ LLM interface connection successful")
            return True
        else:
            print("❌ LLM interface connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing LLM interface: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 GGUF Setup Test Suite")
    print("=" * 60)
    
    tests = [
        ("GGUF Dependencies", test_gguf_imports),
        ("Model Path", test_model_path),
        ("GGUF Provider", test_gguf_provider),
        ("LLM Manager", test_llm_manager),
        ("Text Generation", test_generation),
        ("LLM Interface", test_llm_interface)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! GGUF setup is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 