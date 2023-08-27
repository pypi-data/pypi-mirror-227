from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Image-Processing-Testando-O-Primeiro",
    version="0.0.1",
    author="Wesley Kadekaro",
    author_email="kadekaroshop@gmail.com",
    description="Aprendendo a fazer a criação de pacotes em Python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kadekaro/Descomplicando-A-Criacao-de-Pacotes-em-Python/tree/master",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
