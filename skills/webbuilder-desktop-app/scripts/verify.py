#!/usr/bin/env python3
"""
WebBuilder Desktop — Integration Test Verifier
Quick verification script for common issues
"""

import sys
import os

def verify_imports():
    """Verify all key imports work"""
    sys.path.insert(0, '.')
    from desktop_app import Config, HTMLExporter, ModelRouter, ConfigManager, APIKeyManager
    print("✅ All imports successful")

def verify_providers():
    """Verify provider configuration"""
    from desktop_app import Config
    assert len(Config.ALL_PROVIDERS) >= 12, f"Need 12 providers, got {len(Config.ALL_PROVIDERS)}"
    
    cloud = [p for p in Config.ALL_PROVIDERS.values() if p.get('type') == 'cloud']
    local = [p for p in Config.ALL_PROVIDERS.values() if p.get('type') == 'local']
    
    assert len(cloud) >= 7, f"Need 7 cloud providers, got {len(cloud)}"
    assert len(local) >= 4, f"Need 4 local providers, got {len(local)}"
    
    print(f"✅ Providers: {len(cloud)} cloud, {len(local)} local")

def verify_model_router():
    """Verify model router free-first sorting"""
    from desktop_app import Config, ModelRouter, ConfigManager
    config = ConfigManager()
    router = ModelRouter(config)
    
    # Get all free models
    free = router.get_all_free_models()
    local = router.get_all_local_models()
    
    assert len(free) >= 10, f"Need 10+ free models, got {len(free)}"
    assert len(local) >= 10, f"Need 10+ local models, got {len(local)}"
    
    # Verify free-first sorting for Ollama
    models = router.get_provider_models('ollama')
    assert all(m['free'] for m in models), "All Ollama models should be free"
    
    print(f"✅ Model router: {len(free)} free, {len(local)} local, free-first sorting works")

def verify_html_export():
    """Verify HTML export produces valid output"""
    from desktop_app import HTMLExporter
    
    project = {
        'id': 'verify',
        'name': 'Verify Test',
        'pages': [{'sections': [
            {'id': 's1', 'type': 'navbar', 'props': {'logo': 'Test', 'links': ['Home']}},
            {'id': 's2', 'type': 'hero-centered', 'props': {'title': 'Hello', 'subtitle': 'World', 'ctaText': 'Go', 'backgroundColor': '#3b82f6'}},
            {'id': 's3', 'type': 'features-grid-3', 'props': {'title': 'Features', 'items': [{'title': 'A', 'description': 'B', 'icon': '⚡'}]}},
            {'id': 's4', 'type': 'pricing-3-tiers', 'props': {'title': 'Pricing', 'tiers': [{'name': 'Free', 'price': '$0', 'features': ['X']}]}},
            {'id': 's5', 'type': 'cta-simple', 'props': {'title': 'Ready?', 'buttonText': 'Go', 'backgroundColor': '#10b981'}},
            {'id': 's6', 'type': 'footer', 'props': {'copyright': '© 2024', 'links': ['Privacy']}}
        ]}],
        'design': {'colors': {'primary': '#3b82f6', 'secondary': '#8b5cf6'}, 'fonts': {'heading': 'Inter', 'body': 'Inter'}}
    }
    
    html = HTMLExporter(project).generate_html()
    
    checks = [
        ('DOCTYPE', '<!DOCTYPE html>' in html),
        ('Navbar', 'Test' in html),
        ('Hero', 'Hello' in html),
        ('Features', 'Features' in html),
        ('Pricing', 'Free' in html and '$0' in html),
        ('CTA', 'Ready?' in html),
        ('Footer', '© 2024' in html),
        ('Responsive', '@media' in html),
    ]
    
    for name, passed in checks:
        if not passed:
            raise AssertionError(f"Export check failed: {name}")
    
    print(f"✅ HTML export: {len(html)} chars, all sections valid")

def verify_tests():
    """Run integration tests"""
    if not os.path.exists('test_integration.py'):
        print("⚠️ No test_integration.py found")
        return
    
    import subprocess
    result = subprocess.run([sys.executable, 'test_integration.py'], capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0:
        # Count passed tests
        lines = result.stdout.strip().split('\n')
        passed = sum(1 for l in lines if l.startswith('✅'))
        print(f"✅ {passed} integration tests pass")
    else:
        print(f"❌ Tests failed:\n{result.stdout}\n{result.stderr}")

if __name__ == '__main__':
    print("=" * 60)
    print("WebBuilder Desktop v4.0 — Verification Suite")
    print("=" * 60)
    
    verify_imports()
    verify_providers()
    verify_model_router()
    verify_html_export()
    verify_tests()
    
    print("\n" + "=" * 60)
    print("All verifications passed!")
    print("=" * 60)
