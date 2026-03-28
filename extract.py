#!/usr/bin/env python3
"""
extract.py -- Extract provisioning profile from iOS app
Usage: python3 extract.py app.ipa
       python3 extract.py app.app  (macOS app bundle)
"""
import sys, zipfile, tempfile, subprocess, os
from pathlib import Path

def extract_from_ipa(ipa_path):
    """Extract provisioning profile from IPA"""
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(ipa_path, 'r') as z:
            z.extractall(tmpdir)
        
        # Find .app bundle
        app_dirs = list(Path(tmpdir).rglob("*.app"))
        if not app_dirs:
            print("No .app found in IPA")
            return None
        
        app_dir = app_dirs[0]
        profile = app_dir / "embedded.mobileprovision"
        
        if profile.exists():
            return profile.read_bytes()
    return None

def extract_from_app_bundle(app_path):
    """Extract from macOS/iOS app bundle"""
    profile = Path(app_path) / "embedded.mobileprovision"
    if profile.exists():
        return profile.read_bytes()
    return None

def analyze_profile(profile_data):
    """Parse provisioning profile plist"""
    import plistlib
    try:
        plist = plistlib.loads(profile_data)
        return {
            'name': plist.get('Name', ''),
            'team_id': plist.get('TeamIdentifier', [''])[0],
            'bundle_id': plist.get('Entitlements', {}).get('application-identifier', ''),
            'expires': plist.get('ExpirationDate', ''),
            'devices': plist.get('ProvisionedDevices', []),
            'entitlements': plist.get('Entitlements', {}),
        }
    except Exception as e:
        print(f"Failed to parse: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract.py <app.ipa|app.app>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)
    
    print(f"\n📱 Extracting provisioning profile from {path.name}")
    
    if path.suffix == '.ipa':
        profile_data = extract_from_ipa(str(path))
    else:
        profile_data = extract_from_app_bundle(str(path))
    
    if not profile_data:
        print("No provisioning profile found")
        sys.exit(1)
    
    # Save profile
    out_path = Path(path.stem + ".mobileprovision")
    out_path.write_bytes(profile_data)
    print(f"✅ Saved: {out_path}")
    
    # Analyze
    info = analyze_profile(profile_data)
    if info:
        print(f"\nProfile info:")
        print(f"  Name: {info['name']}")
        print(f"  Team ID: {info['team_id']}")
        print(f"  Expires: {info['expires']}")
        if info['devices']:
            print(f"  Devices: {len(info['devices'])}")

if __name__ == "__main__":
    main()
