# Distribution & Packaging

## PyInstaller Build Script (Verified Working)

```bash
# Full PyInstaller build — verified working with PyQt5 + aiohttp + qrcode + cryptography
# Produces a single standalone .exe with no console window

# Step 1: Build the standalone executable
.\.venv\Scripts\python.exe -m PyInstaller \
  --clean --noconfirm \
  --onefile --windowed \
  --name "VM-Harness" \
  --uac-admin \
  --add-data ".vmharness_signing_key;." \
  --add-data "gui;gui" \
  --add-data "src;src" \
  --hidden-import PyQt5 \
  --hidden-import PyQt5.QtWidgets \
  --hidden-import PyQt5.QtCore \
  --hidden-import PyQt5.QtGui \
  --hidden-import aiohttp \
  --hidden-import qrcode \
  --hidden-import cryptography \
  --hidden-import cryptography.hazmat.primitives \
  --hidden-import asyncssh \
  --hidden-import psutil \
  --hidden-import pydantic \
  --hidden-import pydantic_settings \
  --hidden-import python_dotenv \
  --hidden-import loguru \
  --hidden-import matplotlib \
  --hidden-import docker \
  --hidden-import kubernetes \
  --hidden-import PIL \
  --hidden-import PIL.Image \
  --hidden-import PIL.ImageDraw \
  gui/__main__.py

# Output: dist/VM-Harness.exe (single file, no console, admin-elevated)
```

### Icon Generation (PNG → ICO)

```python
# Generate .ico from largest PNG icon
from PIL import Image
img = Image.open('android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png')
img.save('vm-harness.ico', format='ICO', sizes=[(48,48), (72,72), (96,96), (144,144), (192,192)])
```

### NSIS Installation

```bash
# Install NSIS via winget
winget install NSIS.NSIS --accept-source-agreements --accept-package-agreements

# Build installer
"C:\Program Files (x86)\NSIS\makensis.exe" /V2 installer.nsi

# Output: VM-Harness-Installer.exe
```

**Pitfall**: Do NOT reference bitmap files in NSIS `!define` lines unless they exist on disk. Comment out `MUI_HEADERIMAGE_BITMAP` and `MUI_WELCOMEFINISHPAGE_BITMAP` if the .bmp files are not generated. NSIS will abort with `File: "xxx.bmp" -> no files found` if the referenced bitmap is missing.

## NSIS Installer Script (Full Production-Grade)

```nsis
; VM-Harness Installer — NSIS script
; Builds VM-Harness-Installer.exe

!define PRODUCT_NAME "VM-Harness"
!define PRODUCT_VERSION "2.0.0"
!define PRODUCT_PUBLISHER "VM-Harness Team"
!define PRODUCT_WEB_SITE "https://github.com/LoopyLuci/VM-Harness"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\VM-Harness.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define MUTEX_NAME "Global\VM-Harness-GUI-SingleInstance"

!include "MUI.nsh"
!include "LogicLib.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "vm-harness.ico"
!define MUI_UNICON "vm-harness.ico"
!define MUI_HEADERIMAGE
; !define MUI_HEADERIMAGE_BITMAP "vm-header.bmp"   ; Only if file exists
!define MUI_HEADERIMAGE_RIGHT
; !define MUI_WELCOMEFINISHPAGE_BITMAP "vm-welcome.bmp"  ; Only if file exists

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\VM-Harness.exe"
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "VM-Harness-Installer.exe"
InstallDir "$PROGRAMFILES64\VM-Harness"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show
RequestExecutionLevel admin

; Check for running instance before install
Function .onInit
  System::Call 'kernel32::CreateMutexW(i 0, i 0, t "${MUTEX_NAME}") i .r0'
  System::Call 'kernel32::GetLastError() i .r1'
  ${If} $r1 == 183  ; ERROR_ALREADY_EXISTS
    MessageBox MB_OK|MB_ICONEXCLAMATION "VM-Harness is already running. Please close it before installing."
    Abort
  ${EndIf}
  StrCpy $R0 $r0
FunctionEnd

Section "!VM-Harness Application" SEC01
  SectionIn RO
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File "dist\VM-Harness.exe"
  File "vm-harness.ico"
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\VM-Harness.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\vm-harness.ico"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"

  CreateDirectory "$SMPROGRAMS\VM-Harness"
  CreateShortCut "$SMPROGRAMS\VM-Harness\VM-Harness.lnk" "$INSTDIR\VM-Harness.exe" "" "$INSTDIR\vm-harness.ico" 0
  CreateShortCut "$SMPROGRAMS\VM-Harness\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\vm-harness.ico" 0
  CreateShortCut "$DESKTOP\VM-Harness.lnk" "$INSTDIR\VM-Harness.exe" "" "$INSTDIR\vm-harness.ico" 0
SectionEnd

Section "Start Menu Shortcuts" SEC02
  CreateDirectory "$SMPROGRAMS\VM-Harness"
  CreateShortCut "$SMPROGRAMS\VM-Harness\VM-Harness.lnk" "$INSTDIR\VM-Harness.exe" "" "$INSTDIR\vm-harness.ico" 0
  CreateShortCut "$SMPROGRAMS\VM-Harness\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\vm-harness.ico" 0
SectionEnd

Section "Desktop Shortcut" SEC03
  CreateShortCut "$DESKTOP\VM-Harness.lnk" "$INSTDIR\VM-Harness.exe" "" "$INSTDIR\vm-harness.ico" 0
SectionEnd

Section -Post
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\VM-Harness.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\vm-harness.ico"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  System::Call 'kernel32::CloseHandle(i $R0)'
SectionEnd

Section Uninstall
  Delete "$SMPROGRAMS\VM-Harness\VM-Harness.lnk"
  Delete "$SMPROGRAMS\VM-Harness\Uninstall.lnk"
  RMDir "$SMPROGRAMS\VM-Harness"
  Delete "$DESKTOP\VM-Harness.lnk"
  Delete "$INSTDIR\VM-Harness.exe"
  Delete "$INSTDIR\Uninstall.exe"
  Delete "$INSTDIR\vm-harness.ico"
  DeleteRegKey HKLM "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  RMDir "$INSTDIR"
SectionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove ${PRODUCT_NAME} and all of its components?" IDYES +2
  Abort
FunctionEnd
```

## Portable ZIP Distribution

```python
def create_portable_version():
    portable_dir = "dist/WebBuilder-Portable"
    os.makedirs(portable_dir, exist_ok=True)
    shutil.copy("dist/WebBuilder.exe", portable_dir)
    
    readme = """# WebBuilder Desktop - Portable Version

## Quick Start
1. Run WebBuilder.exe
2. No installation required
3. All data stored in ~/.webbuilder/

## System Requirements
- Windows 10/11 (64-bit)
- 4 GB RAM minimum
- 500 MB disk space
"""
    
    with open(f"{portable_dir}/README.txt", "w") as f:
        f.write(readme)
    
    with zipfile.ZipFile("dist/WebBuilder-Portable-v1.0.0.zip", "w") as zf:
        for root, dirs, files in os.walk(portable_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, portable_dir)
                zf.write(file_path, arcname)
```

## Build Outputs

```
dist/
  WebBuilder.exe - Standalone executable
  WebBuilder-Setup.exe - Windows installer (requires NSIS)
  WebBuilder-Portable-v1.0.0.zip - Portable ZIP
```

## Requirements

```txt
# requirements.txt
PyQt5>=5.15.0
PyQtWebEngine>=5.15.0
numpy>=1.21.0
aiohttp>=3.8.0
PyJWT>=2.0.0
Flask>=2.0.0
Flask-SQLAlchemy>=3.0.0
Flask-Login>=0.6.0
Flask-Limiter>=3.0.0
Flask-CORS>=4.0.0
Werkzeug>=2.0.0
```

## Distribution Checklist

- [ ] Run `python build.py` to create executable
- [ ] Test executable on clean Windows machine
- [ ] Create NSIS installer (install NSIS from nsis.sourceforge.io)
- [ ] Create portable ZIP
- [ ] Test portable version
- [ ] Verify all data files are included (templates, assets)
- [ ] Sign executable with code signing certificate (optional)

## Distribution Pitfalls

- **GitHub URL must match actual remote**: The user renamed the repo from `QEMU-MCP` to `VM-Harness`. Always verify the actual GitHub URL before writing it into installer scripts, updater scripts, or documentation. The correct URL is `https://github.com/LoopyLuci/VM-Harness`. An incorrect URL in the installer means updates will fail silently.

- **Icon size verification via math, not vision**: When generating icons with PIL, the visual proportion of elements (e.g., monitor screens) must be verified by computing actual pixel dimensions, NOT by relying on `vision_analyze` which may return cached/stale results. Use `python3 -c "size=192; w=int(size*0.75); print(f'{w}/{size}={w/size*100:.0f}%')"` to confirm proportions match the user's intent.

- **Project venv isolation**: NEVER use the Hermes venv (`C:/Users/Server/AppData/Local/hermes/hermes-agent/venv/`) for project code. Create a project venv with `python -m venv .venv` in the project root and install all dependencies there. The project must be fully self-contained.

- **Only .exe runs**: Never create `.bat` launcher files. The user explicitly rejected them. Use `.venv/Scripts/pythonw.exe` directly — it's already an executable that suppresses the console window. The user expects a proper installer executable (`App-Installer.exe`), NOT a `.bat` wrapper or a bare PyInstaller output.
