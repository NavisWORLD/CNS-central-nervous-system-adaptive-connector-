# CNS Bridge Apps and Installers

The repository now includes reproducible packaging for desktop and mobile distribution. The packaging workflow is `.github/workflows/packaged-release.yml`.

## Windows

Release artifact: `CNS-Bridge-Setup-Windows-x64.exe`

The workflow:
1. verifies the SHA-256 of the certified Python wheel;
2. installs that wheel on a clean Windows runner;
3. packages `apps/desktop/cns_bridge_desktop.py` with PyInstaller;
4. runs the packaged `CNSBridge.exe --self-test`;
5. wraps the executable with Inno Setup;
6. silently installs the produced installer into a temporary clean directory; and
7. runs the installed executable's self-test.

This is a real one-click Windows installer. It installs per-user by default and does not require administrator privileges.

## macOS

Release artifact: `CNS-Bridge-macOS.dmg`

The workflow verifies the certified wheel, builds a native `.app` bundle with PyInstaller, executes its CNS self-test, creates a DMG, mounts the produced DMG, and executes the app directly from the mounted image.

The public DMG is unsigned. Organizations that require Gatekeeper notarization should sign/notarize the app with their own Apple Developer identity before redistribution.

## Android

Release artifact: `CNS-Bridge-Android.apk`

The mobile companion is implemented with Flutter under `apps/mobile/`. CI generates the Android platform shell, runs static analysis and tests, builds a release APK, installs it into an Android emulator, launches the package, and verifies that the process is alive.

## iPhone / iOS

Release artifacts:
- `CNS-Bridge-iOS-Simulator.app.zip`
- `CNS-Bridge-iOS-Unsigned.app.zip`

CI generates the iOS platform shell, analyzes/tests the Flutter app, builds the release simulator app, boots an available iPhone simulator, installs and launches the app, and then builds an unsigned device app bundle.

Apple requires code signing for installation on physical iPhones and for TestFlight/App Store distribution. The repository therefore publishes an unsigned device bundle that a developer or organization can sign with its own Apple Developer credentials. This is an Apple platform requirement, not a missing CNS feature.

## Mobile CNS contract

The Flutter companion preserves the public interchange contract:

- 12-value sensory state
- 42-value context state
- 54-value recurrent adaptive state
- repeated cycles carry recurrent state forward

The mobile implementation is an interoperable companion implementation. It is not represented as a byte-for-byte port of the NumPy transformer and does not change the scientific boundaries documented elsewhere in the repository.

## GitHub Release

On a successful push to `main`, the packaged release workflow builds all platform artifacts and creates or updates release `v0.1.0`. It attaches Windows, macOS, Android, iOS, Python wheel, release notes, and a combined `SHA256SUMS-ALL` file.

Pull requests run the same platform build/test jobs but do not publish a GitHub Release. This makes packaging failures visible before merge.
