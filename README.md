# 📱 iOS Provisioning Profile Tools

Extract and analyze iOS provisioning profiles (.mobileprovision) — entitlements, certificates, team details.

## Usage

```bash
python3 extract.py app.ipa          # Extract from IPA
python3 analyze.py profile.mobileprovision
python3 list_entitlements.py app.app
```

## What it extracts
- Team ID and team name
- Bundle identifier
- Certificate info (common name, expiry)
- All entitlements
- Development devices (UDIDs for development profiles)
- Expiration dates
