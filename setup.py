from setuptools import find_packages, setup

with open("requirements/requirements.txt") as install_requires_file:
    requirements = install_requires_file.read().strip().split("\n")

setup(
    name="rag-chatbot-banks",
    description="Rag Chatbot",
    license="Apache License 2.0",
    author="Prefect Community",
    author_email="hello@prefect.io",
    keywords="prefect",
    long_description_content_type="text/markdown",
    version="1.0",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.12",
    install_requires=requirements,
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
    ],
)
