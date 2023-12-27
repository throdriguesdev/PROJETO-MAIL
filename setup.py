from cx_Freeze import setup, Executable

setup(
    name="EmailTelecom",
    version="1.0",
    description="Versão Executavel",
    executables=[Executable("main.py")],
)
