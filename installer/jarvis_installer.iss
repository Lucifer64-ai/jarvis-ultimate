; JARVIS Ultimate Installer Script
; Inno Setup Configuration

#define MyAppName "JARVIS Ultimate"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Lucifer64-ai"
#define MyAppURL "https://github.com/Lucifer64-ai/jarvis-ultimate"
#define MyAppExeName "jarvis.exe"

[Setup]
; App Identity
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Default Installation Directory
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

; Output Settings
OutputDir=output
OutputBaseFilename=JARVIS_Ultimate_Setup_{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

; Visual Settings
; WizardImageFile=assets\jarvis_installer.bmp  ; ÃÃÃÂ¤ÃÃÃÂ°ÃÃÃÂ¹ÃÃÃÂ» ÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ²ÃÃÃÃÃÂµÃÃ
; WizardSmallImageFile=assets\jarvis_installer_small.bmp  ; ÃÃÃÂ¤ÃÃÃÂ°ÃÃÃÂ¹ÃÃÃÂ» ÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ²ÃÃÃÃÃÂµÃÃ
SetupIconFile=..\assets\jarvis.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Privilege & Architecture
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; License & Info
LicenseFile=..\LICENSE
InfoBeforeFile=installer\install_notes.txt

; Language
LanguageDetectionMethod=uilanguage
ShowLanguageDialog=auto

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "autostart"; Description: "ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ°ÃÃÃÃÃÃÃÃÃÂ¿ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂºÃÃÃÃÃÃÃÃÃÂ°ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃ JARVIS ÃÃÃÃÃÃÃÃÃÂ¿ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¸ ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ°ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂµ Windows"; GroupDescription: "ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÂ¿ÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÂ»ÃÃÃÃÃÃÃÃÃÂ½ÃÃÃÃÃÃÃÃÃÂ¸ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂµÃÃÃÃÃÃÃÃÃÂ»ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ½ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂµ ÃÃÃÃÃÃÃÃÃÂ½ÃÃÃÃÃÃÃÃÃÂ°ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÂ¹ÃÃÃÃÃÃÃÃÃÂºÃÃÃÃÃÃÃÃÃÂ¸:"; Flags: unchecked
Name: "cleanmode"; Description: "ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂºÃÃÃÃÃÃÃÃÃÂ»ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¸ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃ ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂµÃÃÃÃÃÃÃÃÃÂ¶ÃÃÃÃÃÃÃÃÃÂ¸ÃÃÃÃÃÃÃÃÃÂ¼ ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¸ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÂ³ÃÃÃÃÃÃÃÃÃÂ¾ ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ°ÃÃÃÃÃÃÃÃÃÂ±ÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂµÃÃÃÃÃÃÃÃÃÂ³ÃÃÃÃÃÃÃÃÃÂ¾ ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÂ»ÃÃÃÃÃÃÃÃÃÂ°"; GroupDescription: "ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÂ¿ÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÂ»ÃÃÃÃÃÃÃÃÃÂ½ÃÃÃÃÃÃÃÃÃÂ¸ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂµÃÃÃÃÃÃÃÃÃÂ»ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ½ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂµ ÃÃÃÃÃÃÃÃÃÂ½ÃÃÃÃÃÃÃÃÃÂ°ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÂ¹ÃÃÃÃÃÃÃÃÃÂºÃÃÃÃÃÃÃÃÃÂ¸:"; Flags: unchecked

[Files]
; Main Application - all files from package
Source: "installer\package\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ°ÃÃÃÃÃÃÃÃÃÂ¿ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¸ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃ JARVIS Ultimate"; Flags: nowait postinstall skipifsilent
Filename: "{app}\docs\README.md"; Description: "ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂºÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃ ÃÃÃÃÃÃÃÃÃÂ´ÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÂºÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¼ÃÃÃÃÃÃÃÃÃÂµÃÃÃÃÃÃÃÃÃÂ½ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ°ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¸ÃÃÃÃÃÃÃÃ"; Flags: shellexec skipifsilent

[UninstallRun]
; Cleanup on uninstall
Filename: "{cmd}"; Parameters: "/c rmdir /s /q ""{app}\data"""; Flags: runhidden
Filename: "{cmd}"; Parameters: "/c rmdir /s /q ""{app}\logs"""; Flags: runhidden

[Registry]
; Auto-start registry entry
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "JARVIS Ultimate"; ValueData: """{app}\{#MyAppExeName}"""; Tasks: autostart

; Application settings
Root: HKCU; Subkey: "Software\{#MyAppName}"; ValueType: none; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppName}\Settings"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKCU; Subkey: "Software\{#MyAppName}\Settings"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"
Root: HKCU; Subkey: "Software\{#MyAppName}\Settings"; ValueType: dword; ValueName: "CleanMode"; ValueData: "1"; Tasks: cleanmode

[Dirs]
Name: "{app}\data"
Name: "{app}\logs"
Name: "{app}\plugins"
Name: "{app}\models"
Name: "{app}\backups"

[Code]
function InitializeUninstall(): Boolean;
begin
  Result := MsgBox('ÃÃÃÃÃÃÃÃ ÃÃÃÃÃÂ´ÃÃÃÃÃÂµÃÃÃÃÃÂ¹ÃÃÃÃÃÃÃÃÃÃÃÃÃÂ²ÃÃÃÃÃÂ¸ÃÃÃÃÃÃÃÃÃÂµÃÃÃÃÃÂ»ÃÃÃÃÃÃÃÃÃÂ½ÃÃÃÃÃÂ¾ ÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÃÃÃÃÂ¸ÃÃÃÃÃÃÃÃÃÂµ ÃÃÃÃÃÃÃÃÃÂ´ÃÃÃÃÃÂ°ÃÃÃÃÃÂ»ÃÃÃÃÃÂ¸ÃÃÃÃÃÃÃÃ JARVIS Ultimate?' + #13#10 + #13#10 +
                   'ÃÃÃÃÃÃÃÃÃÃÃÃÃÂµ ÃÃÃÃÃÂ½ÃÃÃÃÃÂ°ÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÃÂ¾ÃÃÃÃÃÂ¹ÃÃÃÃÃÂºÃÃÃÃÃÂ¸ ÃÃÃÃÃÂ¸ ÃÃÃÃÃÂ´ÃÃÃÃÃÂ°ÃÃÃÃÃÂ½ÃÃÃÃÃÂ½ÃÃÃÃÃÃÃÃÃÂµ ÃÃÃÃÃÂ±ÃÃÃÃÃÃÃÃÃÂ´ÃÃÃÃÃÃÃÃ ÃÃÃÃÃÃÃÃÃÂ´ÃÃÃÃÃÂ°ÃÃÃÃÃÂ»ÃÃÃÃÃÂµÃÃÃÃÃÂ½ÃÃÃÃ.', 
                   mbConfirmation, MB_YESNO) = IDYES;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    // Remove auto-start entry
    RegDeleteValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Run', 'JARVIS Ultimate');
  end;
end;
