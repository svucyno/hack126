import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dripfit.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
import json

def run_tests():
    print("Starting tests...\n")
    
    # 1. Create a test user
    User.objects.filter(username="testuser").delete()
    user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
    print(f"[*] Created test user: {user.email}")
    
    # 2. Test unauthenticated request
    client = Client()
    response = client.get('/api/auth/status/')
    print(f"[*] Unauthenticated /api/auth/status/: {response.json()}")
    
    # 3. Log in and test authenticated request
    client.force_login(user)
    response = client.get('/api/auth/status/')
    print(f"[*] Authenticated /api/auth/status/: {response.json()}")
    
    response = client.get('/api/auth/profile/')
    print(f"[*] Profile FETCH: {response.status_code}")
    
    # 4. Test Style Me Engine (Module 2) - relies on Sample Dataset instead of wardrobe
    # Request body matching what we defined in outfits/views.py
    data = {
        "skin_tone": 4, 
        "occasion": "casual",
        "figure_type": "female"
    }
    print(f"\nRunning out Outfit Engine (Style Me Module) with: {data}...")
    
    response = client.post('/api/outfit/style-me/', data=json.dumps(data), content_type="application/json")
    print(f"Engine Response Status: {response.status_code}")
    
    result = response.json()
    if response.status_code == 200:
        stats = result.get('engine_stats', {})
        best = result.get('best_outfit')
        print(f"[*] Engine completed successfully!")
        print(f"   - Combinations built: {stats.get('combinations_built')}")
        print(f"   - Passed balancer: {stats.get('after_balancer')}")
        if best:
            print(f"   - Best Outfit Persona: {best.get('persona')}")
            print(f"   - Best Outfit Score: {best.get('score', {}).get('total')}/100")
            print(f"   - Items chosen:")
            for k, v in best.get('items', {}).items():
                 print(f"      {k}: {v.get('colour_name')} {v.get('item_subtype')} ({v.get('pattern')})")
        else:
            print(f"   [!] No outfit returned. Error: {result.get('error')}")
    else:
        print(f"   [!] Engine failed with: {result}")
        
    print("\nAll tests finished!")

if __name__ == '__main__':
    run_tests()
