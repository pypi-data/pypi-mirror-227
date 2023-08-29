from setuptools import setup, find_packages

setup(
    name="label_mapper",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.0",
    ],
    author="WJB Mattingly",
    description="A spaCy extension to map NER labels.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)
