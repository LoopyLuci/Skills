# Production Readiness for Tauri 2 Apps

Session-proven patterns for packaging, documenting, and distributing Tauri 2 desktop applications.

## Packaging

### Windows (MSI/NSIS)

**Prerequisites:**
- Visual Studio Build Tools (C++ workload)
- Windows SDK

**Build command:**
```bash
cargo tauri build --target x86_64-pc-windows-msvc
```

**Output locations:**
- MSI: `src-tauri/target/release/bundle/msi/DiskRipper_0.1.0_x64_en-US.msi`
- NSIS: `src-tauri/target/release/bundle/nsis/DiskRipper_0.1.0_x64-setup.exe`

**Packaging script (`scripts/package.ps1`):**
```powershell
# Build frontend
Set-Location ../frontend
npm install
npm run build

# Build Rust + Tauri
Set-Location ../diskripper-tauri
cargo tauri build

# Copy to output directory
$OutputDir = "../packages"
New-Item -ItemType Directory -Force -Path $OutputDir
Copy-Item -Path "src-tauri/target/release/bundle/*" -Destination $OutputDir -Recurse

# Create checksums
Get-ChildItem -Path $OutputDir -Include *.msi,*.exe -Recurse | ForEach-Object {
    $hash = Get-FileHash $_.FullName -Algorithm SHA256
    "$($hash.Hash)  $($_.Name)" | Out-File -Append -FilePath "$OutputDir/checksums.txt"
}
```

### Linux (AppImage/DEB)

**Prerequisites:**
```bash
sudo apt install libgtk-3-dev libwebkit2gtk-4.0-dev libayatana-appindicator3-dev librsvg2-dev
```

**Build command:**
```bash
cargo tauri build --target x86_64-unknown-linux-gnu
```

**Output locations:**
- AppImage: `src-tauri/target/release/bundle/appimage/diskripper_0.1.0_amd64.AppImage`
- DEB: `src-tauri/target/release/bundle/deb/diskripper_0.1.0_amd64.deb`

**Packaging script (`scripts/package.sh`):**
```bash
#!/bin/bash
set -e

# Build frontend
cd ../frontend
npm install
npm run build

# Build Rust + Tauri
cd ../diskripper-tauri
cargo tauri build

# Copy to output
mkdir -p ../packages
cp -r src-tauri/target/release/bundle/* ../packages/

# Create checksums
cd ../packages
find . -type f \( -name "*.AppImage" -o -name "*.deb" -o -name "*.rpm" \) -exec sha256sum {} \; > checksums.txt
```

### macOS (DMG)

**Build command:**
```bash
# Intel
cargo tauri build --target x86_64-apple-darwin

# Apple Silicon
cargo tauri build --target aarch64-apple-darwin
```

**Output location:**
- DMG: `src-tauri/target/release/bundle/dmg/DiskRipper_0.1.0_aarch64.dmg`

### Icons

Required icon files in `src-tauri/icons/`:
- `32x32.png` — 32x32 pixels
- `128x128.png` — 128x128 pixels
- `128x128@2x.png` — 256x256 pixels (Retina)
- `icon.icns` — macOS icon set
- `icon.ico` — Windows icon

**Generate icons from a single PNG:**
```bash
# macOS
sips -Z 32 icon.png --out icons/32x32.png
sips -Z 128 icon.png --out icons/128x128.png
sips -Z 256 icon.png --out icons/128x128@2x.png

# Windows ICO (requires ImageMagick)
convert icon.png -define icon:auto-resize=256,128,64,32,16 icons/icon.ico

# macOS ICNS (requires iconutil)
mkdir icon.iconset
sips -Z 16 icon.png --out icon.iconset/icon_16x16.png
sips -Z 32 icon.png --out icon.iconset/icon_16x16@2x.png
# ... (all sizes)
iconutil -c icns icon.iconset -o icons/icon.icns
```

### tauri.conf.json Bundle Configuration

```json
{
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ],
    "resources": [],
    "externalBin": [],
    "copyright": "2026 Author Name",
    "category": "Utility",
    "shortDescription": "Brief app description",
    "longDescription": "Longer description for app stores",
    "windows": {
      "certificateThumbprint": null,
      "digestAlgorithm": "sha256",
      "timestampUrl": ""
    },
    "linux": {
      "deb": {
        "depends": []
      }
    },
    "macOS": {
      "frameworks": [],
      "minimumSystemVersion": "10.15",
      "exceptionDomain": "",
      "signingIdentity": "",
      "providerShortName": "",
      "entitlements": null
    }
  }
}
```

## User Documentation

### Structure

```
docs/
  USER_GUIDE.md           # Main user documentation
  DEMO_VIDEO_SCRIPT.md    # Video script for demos
  FEEDBACK_SYSTEM.md      # Feedback collection design
```

### User Guide Sections

1. **Quick Start** — Installation + first launch
2. **User Guide** — Feature-by-feature walkthrough
3. **FAQ** — Common questions
4. **Troubleshooting** — Known issues and fixes

### Quick Start Template

```markdown
## Quick Start

### Installation

#### Windows
1. Download `DiskRipper-0.1.0-x64.msi` from Releases
2. Run installer and follow prompts
3. Launch from Start Menu

#### macOS
1. Download `DiskRipper-0.1.0.dmg` from Releases
2. Open DMG and drag to Applications
3. Launch from Applications

#### Linux
**AppImage:**
chmod +x DiskRipper-0.1.0.AppImage
./DiskRipper-0.1.0.AppImage

### First Launch
1. Insert optical disc
2. Open DiskRipper
3. Click Refresh to detect drive
4. Select drive and action
5. Set output path
6. Start operation
```

### FAQ Template

```markdown
## FAQ

**Q: What disc types are supported?**
A: CD-ROM, CD-R, CD-RW, DVD-ROM, DVD-R, DVD-RW, DVD+R, DVD+RW, DVD-RAM, DVD+R DL, BD-ROM, BD-R, BD-RE, BD-R DL, HD DVD.

**Q: Can I rip copy-protected discs?**
A: Structural protections (bad sectors, hidden tracks) are handled. CSS/AACS decryption requires system libraries (libdvdcss, libaacs).

**Q: Why is my rip failing?**
A: Common causes: scratched disc, dirty lens, incompatible drive, insufficient disk space.
```

## Demo Video Script

### Structure (3-4 minutes)

| Scene | Time | Content |
|-------|------|---------|
| 1 | 0:00-0:30 | Introduction — what is DiskRipper |
| 2 | 0:30-1:00 | Drive detection |
| 3 | 1:00-1:45 | Creating a disc image |
| 4 | 1:45-2:15 | Extracting files |
| 5 | 2:15-2:45 | Audio CD ripping |
| 6 | 2:45-3:15 | Verification |
| 7 | 3:15-3:45 | Settings & CLI |
| 8 | 3:45-4:00 | Conclusion & links |

### Production Notes

- **Resolution:** 1920x1080, 30fps
- **Audio:** Clean voiceover, no background music
- **Cursor:** Highlight clicks
- **Editing:** Zoom effects on UI elements, smooth transitions
- **Accessibility:** Closed captions, audio description track

### Distribution

- YouTube (primary)
- Vimeo (backup)
- Embedded in documentation
- Social media clips (30-second versions)

## Feedback Collection

### In-App Feedback Dialog

**Component:** `FeedbackDialog.tsx`

**Features:**
- Feedback type selector (Bug/Feature/General)
- Subject line
- Description textarea
- Optional email
- System info toggle
- Log inclusion toggle

**UI Layout:**
```
┌─────────────────────────────────────────┐
│  Send Feedback                          │
├─────────────────────────────────────────┤
│  Type: [Bug Report ▼]                   │
│  Subject: [________________]            │
│  Description:                           │
│  ┌─────────────────────────────────┐    │
│  │                                 │    │
│  └─────────────────────────────────┘    │
│  Email (optional): [______________]     │
│  [✓] Include system information         │
│  [✓] Include log files                  │
│  [Cancel]              [Submit]         │
└─────────────────────────────────────────┘
```

### Backend API

**Endpoints:**
```
POST /api/feedback          — Submit feedback
GET  /api/feedback          — List (admin)
GET  /api/feedback/:id      — Get specific
PUT  /api/feedback/:id      — Update status
DELETE /api/feedback/:id    — Delete
```

**Schema:**
```json
{
  "id": "uuid",
  "type": "bug|feature|general",
  "subject": "String (max 200)",
  "description": "String (max 5000)",
  "system_info": {},
  "screenshot": "base64 (optional)",
  "email": "optional",
  "status": "new|in_progress|resolved|closed",
  "created_at": "ISO 8601",
  "updated_at": "ISO 8601"
}
```

### Implementation Options

| Service | Type | Cost | Setup |
|---------|------|------|-------|
| GitHub Issues | Bug tracking | Free | GitHub API |
| Sentry | Error tracking | Free tier | SDK |
| Formspree | Form handling | Free tier | HTML form |
| Google Forms | Surveys | Free | Embed link |

### Recommended: GitHub Issues Integration

```rust
async fn submit_github_issue(feedback: &Feedback) -> Result<(), Error> {
    let client = reqwest::Client::new();
    let repo = "LoopyLuci/DiskRipper";
    
    let title = format!("[{}] {}", feedback.feedback_type.to_uppercase(), feedback.subject);
    let body = format!(
        "## Description\n{}\n\n## System Info\n```json\n{}\n```\n\n## Feedback ID\n{}",
        feedback.description,
        serde_json::to_string_pretty(&feedback.system_info).unwrap(),
        feedback.id
    );
    
    let issue = serde_json::json!({
        "title": title,
        "body": body,
        "labels": [feedback.feedback_type]
    });
    
    client
        .post(format!("https://api.github.com/repos/{}/issues", repo))
        .header("Authorization", format!("token {}", GITHUB_TOKEN))
        .header("User-Agent", "DiskRipper")
        .json(&issue)
        .send()
        .await?;
    
    Ok(())
}
```

### Privacy Policy

**Collected:**
- App version and OS type
- Drive model and firmware
- User-submitted feedback text
- Optional contact email

**NOT collected:**
- Personal files or contents
- IP addresses (unless required by law)
- Usage patterns (without consent)
- Disc content or metadata

### Store Integration

```typescript
// store.ts
addToast: (type, message) => {
  const id = crypto.randomUUID();
  set((state) => ({ toasts: [...state.toasts, { id, type, message }] }));
  setTimeout(() => get().removeToast(id), 5000);
},

// Listen for backend events
await listen('job:completed', (event) => {
  get().refreshJobs();
  get().addToast('success', 'Job completed');
});
```

## Release Checklist

- [ ] All tests pass (`cargo test --workspace`)
- [ ] No clippy warnings (`cargo clippy --workspace --tests`)
- [ ] Frontend builds (`npm run build`)
- [ ] Backend builds (`cargo build --release`)
- [ ] Tauri bundles successfully (`cargo tauri build`)
- [ ] Icons present in all required sizes
- [ ] Version number updated in all locations
- [ ] CHANGELOG.md updated
- [ ] Git tag created (`git tag v0.1.0`)
- [ ] GitHub Release drafted with artifacts
- [ ] Checksums generated and verified
- [ ] Documentation updated
- [ ] Demo video recorded (optional)
