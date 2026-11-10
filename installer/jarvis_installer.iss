; JARVIS Ultimate Installer Script
; Inno Setup Configuration

#define MyAppName "JARVIS Ultimate"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "JARVIS Team"
#define MyAppURL "https://github.com/Lucifer64-ai/jarvis-ultimate"
#define MyAppExeName "JARVIS.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE
OutputDir=output
OutputBaseFilename=JARVIS_Ultimate_Setup
SetupIconFile=..\assets\jarvis.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "autostart"; Description: "Запускать JARVIS при старте Windows"; GroupDescription: "Дополнительные параметры:"; Flags: unchecked

[Files]
Source: "..\dist\JARVIS\JARVIS.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\JARVIS\config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\JARVIS\.env"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\JARVIS\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Настройки JARVIS"; Filename: "{app}\config.json"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Запустить {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "JARVIS"; ValueData: """{app}\{#MyAppExeName}"""; Tasks: autostart

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('Добро пожаловать в установщик JARVIS Ultimate!' + #13#10 + #13#10 +
         'Этот мастер установит JARVIS на ваш компьютер.' + #13#10 + #13#10 +
         'После установки настройте .env файл для подключения:' + #13#10 +
         '- OpenAI API (опционально)' + #13#10 +
         '- Home Assistant (опционально)',
         mbInformation, MB_OK);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Установка завершена!' + #13#10 + #13#10 +
           'Не забудьте настроить .env файл перед первым запуском.',
           mbInformation, MB_OK);
  end;
end;
