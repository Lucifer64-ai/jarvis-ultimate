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
AppPublisher={#MyAppName}
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
WizardImageFile=assets\jarvis_installer.bmp
WizardSmallImageFile=assets\jarvis_installer_small.bmp
SetupIconFile=assets\jarvis.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Privilege & Architecture
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; License & Info
LicenseFile=LICENSE
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
Name: "autostart"; Description: "Запускать JARVIS при старте Windows"; GroupDescription: "Дополнительные настройки:"; Flags: unchecked
Name: "cleanmode"; Description: "Включить режим чистого рабочего стола"; GroupDescription: "Дополнительные настройки:"; Flags: unchecked

[Files]
; Main Application
Source: "dist\jarvis\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\jarvis.ico"; DestDir: "{app}\assets"; Flags: ignoreversion

; Configuration Files
Source: ".env.example"; DestDir: "{app}"; DestName: ".env"; Flags: onlyifdoesntexist
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "README.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs

; Python Runtime (if bundled)
Source: "python_runtime\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs; Check: IsPythonNotInstalled

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Запустить JARVIS Ultimate"; Flags: nowait postinstall skipifsilent
Filename: "{app}\docs\README.md"; Description: "Открыть документацию"; Flags: shellexec skipifsilent

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
var
  PythonPage: TInputDirWizardPage;
  PythonInstalled: Boolean;

function IsPythonNotInstalled(): Boolean;
var
  PythonPath: String;
begin
  Result := not RegQueryStringValue(HKLM, 'SOFTWARE\Python\PythonCore\3.11\InstallPath', '', PythonPath) and
            not RegQueryStringValue(HKCU, 'SOFTWARE\Python\PythonCore\3.11\InstallPath', '', PythonPath) and
            not RegQueryStringValue(HKLM, 'SOFTWARE\Python\PythonCore\3.10\InstallPath', '', PythonPath) and
            not RegQueryStringValue(HKCU, 'SOFTWARE\Python\PythonCore\3.10\InstallPath', '', PythonPath);
end;

procedure InitializeWizard();
begin
  PythonInstalled := not IsPythonNotInstalled();
  
  if not PythonInstalled then
  begin
    PythonPage := CreateInputDirPage(wpSelectDir,
      'Python не найден', 'Укажите путь к Python 3.10+',
      'JARVIS требует Python 3.10 или выше. Укажите путь к установке Python:',
      False, 'Python 3.10+');
    PythonPage.Add('');
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  PythonPath: String;
begin
  Result := True;
  
  if (CurPageID = PythonPage.ID) and not PythonInstalled then
  begin
    PythonPath := PythonPage.Values[0];
    if not DirExists(PythonPath) then
    begin
      MsgBox('Указанный путь не существует. Пожалуйста, укажите корректный путь к Python.', mbError, MB_OK);
      Result := False;
    end
    else if not FileExists(PythonPath + '\python.exe') then
    begin
      MsgBox('В указанной папке не найден python.exe. Пожалуйста, проверьте путь.', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
  PythonPath: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Install Python dependencies
    if not PythonInstalled then
      PythonPath := PythonPage.Values[0] + '\python.exe'
    else
      PythonPath := 'python';
    
    // Install requirements
    if FileExists(ExpandConstant('{app}\requirements.txt')) then
    begin
      Exec(PythonPath, '-m pip install -r "' + ExpandConstant('{app}\requirements.txt') + '"', 
           '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
    end;
    
    // Initialize configuration
    if not FileExists(ExpandConstant('{app}\.env')) then
    begin
      FileCopy(ExpandConstant('{app}\.env.example'), ExpandConstant('{app}\.env'), False);
    end;
  end;
end;

function InitializeUninstall(): Boolean;
begin
  Result := MsgBox('Вы действительно хотите удалить JARVIS Ultimate?' + #13#10 + #13#10 +
                   'Все настройки и данные будут удалены.', 
                   mbConfirmation, MB_YESNO) = IDYES;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    // Remove auto-start entry
    RegDeleteValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Run', 'JARVIS Ultimate');
    
    // Remove application settings
    RegDeleteKeyIncludingSubkeys(HKCU, 'Software\{#MyAppName}');
  end;
end;
