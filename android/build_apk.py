"""Build the offline Android phone-test APK with the locally installed SDK/JDK."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(os.environ.get("COURIER_ANDROID_TOOLS", r"C:\My Game\tools\android-build"))
JDK = TOOLS / "jdk" / "jdk-21.0.12.1+1" / "bin"
SDK = TOOLS / "sdk"
BUILD_TOOLS = SDK / "build-tools" / "android-16"
ANDROID_JAR = SDK / "platforms" / "android-36" / "android.jar"
BUILD = ROOT / "android" / "build"
STAGE = BUILD / "stage"
OUTPUTS = BUILD / "outputs"
NAME = "Last-Light-Courier-0.1.1-phone-test.apk"


def run(*args: object) -> None:
    command = [str(arg) for arg in args]
    print("Running:", Path(command[0]).name, " ".join(command[1:4]))
    subprocess.run(command, check=True)


def add_files(apk: Path, root: Path) -> None:
    with zipfile.ZipFile(apk, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in root.rglob("*"):
            if file.is_file():
                archive.write(file, file.relative_to(root).as_posix())


def main() -> None:
    subprocess.run([sys.executable, "-B", str(ROOT / "campaign" / "build_levels.py")], check=True)
    source = (ROOT / "CAMPAIGN_100_LEVELS.html").read_text(encoding="utf-8")
    matches = list(re.finditer(r"<script>(.*?)</script>", source, re.S))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one inline game script; found {len(matches)}")
    for required in ("FEEDBACK.emit('step')", "FEEDBACK.emit('house')", "FEEDBACK.emit('repair')", "FEEDBACK.emit('shadowNear')"):
        if required not in matches[0].group(1):
            raise RuntimeError(f"Missing game event: {required}")
    if STAGE.exists():
        shutil.rmtree(STAGE)
    for folder in (STAGE / "assets" / "www", STAGE / "classes", STAGE / "dex", STAGE / "generated", OUTPUTS):
        folder.mkdir(parents=True, exist_ok=True)
    (STAGE / "assets" / "www" / "index.html").write_text(source[:matches[0].start()] + '<script src="game.js"></script>' + source[matches[0].end():], encoding="utf-8")
    (STAGE / "assets" / "www" / "game.js").write_text(matches[0].group(1), encoding="utf-8")
    manifest = ROOT / "android" / "app" / "src" / "main" / "AndroidManifest.xml"
    resources = ROOT / "android" / "app" / "src" / "main" / "res"
    compiled = STAGE / "resources.zip"
    unsigned = STAGE / "unsigned.apk"
    run(BUILD_TOOLS / "aapt2.exe", "compile", "--dir", resources, "-o", compiled)
    run(BUILD_TOOLS / "aapt2.exe", "link", "-o", unsigned, "-I", ANDROID_JAR,
        "--manifest", manifest, "--min-sdk-version", "26", "--target-sdk-version", "34",
        "--version-code", "2", "--version-name", "0.1.1", "--java", STAGE / "generated", compiled)
    with zipfile.ZipFile(unsigned, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in (STAGE / "assets").rglob("*"):
            if file.is_file():
                archive.write(file, file.relative_to(STAGE).as_posix())
    sources = [str(path) for base in (ROOT / "android" / "app" / "src" / "main" / "java", STAGE / "generated") for path in base.rglob("*.java")]
    run(JDK / "javac.exe", "-encoding", "UTF-8", "-source", "8", "-target", "8",
        "-bootclasspath", str(ANDROID_JAR) + ";" + str(BUILD_TOOLS / "core-lambda-stubs.jar"),
        "-d", STAGE / "classes", *sources)
    classes = list((STAGE / "classes").rglob("*.class"))
    run(JDK / "java.exe", "-cp", BUILD_TOOLS / "lib" / "d8.jar", "com.android.tools.r8.D8",
        "--debug", "--lib", ANDROID_JAR, "--min-api", "26", "--output", STAGE / "dex", *classes)
    add_files(unsigned, STAGE / "dex")
    local = ROOT / "android" / ".local"
    local.mkdir(parents=True, exist_ok=True)
    key = local / "phone-test.jks"
    if not key.exists():
        run(JDK / "keytool.exe", "-genkeypair", "-keystore", key, "-storetype", "JKS", "-alias", "androiddebugkey",
            "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000",
            "-dname", "CN=Last Light Courier Phone Test,O=Sydra,C=IN", "-storepass", "android", "-keypass", "android")
    aligned = STAGE / "aligned.apk"
    apk = OUTPUTS / NAME
    run(BUILD_TOOLS / "zipalign.exe", "-f", "-P", "16", "4", unsigned, aligned)
    run(JDK / "java.exe", "-jar", BUILD_TOOLS / "lib" / "apksigner.jar", "sign", "--ks", key,
        "--ks-key-alias", "androiddebugkey", "--ks-pass", "pass:android", "--key-pass", "pass:android",
        "--out", apk, aligned)
    run(BUILD_TOOLS / "zipalign.exe", "-c", "-P", "16", "4", apk)
    run(JDK / "java.exe", "-jar", BUILD_TOOLS / "lib" / "apksigner.jar", "verify", "--verbose", apk)
    with zipfile.ZipFile(apk) as archive:
        assert "assets/www/index.html" in archive.namelist()
        assert "assets/www/game.js" in archive.namelist()
        assert "classes.dex" in archive.namelist()
    digest = hashlib.sha256(apk.read_bytes()).hexdigest()
    print(f"READY {apk}\nSHA256 {digest}\nBYTES {apk.stat().st_size}")


if __name__ == "__main__":
    main()
