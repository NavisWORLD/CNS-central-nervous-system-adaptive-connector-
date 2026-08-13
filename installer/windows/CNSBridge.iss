#define MyAppName "CNS Bridge"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Cory Shane Davis / NavisWORLD"
#define MyAppExeName "CNSBridge.exe"

[Setup]
AppId={{9A42D2A8-2EBB-4BEA-9A3B-35F4A01E4427}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\CNSBridge
DefaultGroupName={#MyAppName}
PrivilegesRequired=lowest
OutputDir=..\..\release
OutputBaseFilename=CNS-Bridge-Setup-Windows-x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}
LicenseFile=..\..\LICENSE

[Files]
Source: "..\..\build\windows\CNSBridge.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
