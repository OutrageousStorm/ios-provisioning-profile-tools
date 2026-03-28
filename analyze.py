#!/usr/bin/env python3
"""
analyze.py -- Detailed provisioning profile analysis
Usage: python3 analyze.py profile.mobileprovision [--json output.json]
"""
import sys, argparse, json, plistlib
from pathlib import Path
from datetime import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile")
    parser.add_argument("--json", help="Export to JSON")
    args = parser.parse_args()
    
    profile_path = Path(args.profile)
    if not profile_path.exists():
        print(f"Profile not found: {profile_path}")
        sys.exit(1)
    
    try:
        plist = plistlib.loads(profile_path.read_bytes())
    except Exception as e:
        print(f"Failed to parse: {e}")
        sys.exit(1)
    
    print(f"\n📱 Provisioning Profile Analysis")
    print("=" * 50)
    
    # Basic info
    print(f"\nBasic Info:")
    print(f"  Name: {plist.get('Name', 'N/A')}")
    print(f"  UUID: {plist.get('UUID', 'N/A')}")
    team_ids = plist.get('TeamIdentifier', [])
    print(f"  Team IDs: {', '.join(team_ids)}")
    print(f"  Expires: {plist.get('ExpirationDate', 'N/A')}")
    
    # Bundle ID from entitlements
    ents = plist.get('Entitlements', {})
    app_id = ents.get('application-identifier', '')
    print(f"  Bundle ID: {app_id}")
    
    # Certificates
    certs = plist.get('DeveloperCertificates', [])
    print(f"\nCertificates: {len(certs)}")
    
    # Devices
    devices = plist.get('ProvisionedDevices', [])
    print(f"\nDevices: {len(devices)}")
    if devices:
        for udid in devices[:5]:
            print(f"  - {udid}")
        if len(devices) > 5:
            print(f"  ... and {len(devices)-5} more")
    
    # Entitlements (first 10)
    print(f"\nEntitlements ({len(ents)}):")
    for k, v in list(ents.items())[:10]:
        v_str = str(v)[:40]
        print(f"  {k}: {v_str}")
    if len(ents) > 10:
        print(f"  ... and {len(ents)-10} more")
    
    # Export
    if args.json:
        export = {
            'name': plist.get('Name'),
            'uuid': plist.get('UUID'),
            'team_ids': team_ids,
            'bundle_id': app_id,
            'expires': str(plist.get('ExpirationDate', '')),
            'device_count': len(devices),
            'entitlements': list(ents.keys()),
        }
        with open(args.json, 'w') as f:
            json.dump(export, f, indent=2)
        print(f"\n✅ Exported to {args.json}")

if __name__ == "__main__":
    main()
