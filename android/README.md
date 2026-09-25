# Android phone-test build

Run `python -B android/build_apk.py` from the repository root. The script builds the current 100-level campaign, packages it offline in a native Android WebView, and signs a phone-test APK in `android/build/outputs/`.

The APK needs Android 8.0 or newer. It requests only vibration permission. No network permission or remote assets are used. Game progress and sound/vibration preferences are saved on the device.

This build uses the local SDK/JDK at `C:\My Game\tools\android-build` by default. Set `COURIER_ANDROID_TOOLS` to another compatible toolchain root if needed. Keep `android/.local/phone-test.jks` for future updates to install over this APK. It is a local testing key, not a production signing key.
