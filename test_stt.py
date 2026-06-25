import subprocess

subprocess.run([
    "python",
    "-m",
    "moonshine_voice.mic_transcriber",
    "--language",
    "en"
])