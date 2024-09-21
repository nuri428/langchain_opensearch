import setuptools

setuptools.setup(
    name="langchain_opensearch",
    version="0.0.2",
    author="jaeho kang",
    author_email="greennuri@gmail.com",
    description="A package for interacting with OpenSearch from LangChain",
    long_description="This package provides a LangChain retriever for OpenSearch.",
    long_description_content_type="text/markdown",
    url="https://github.com/nuri428/langchain_opensearch.git",
    project_url="https://github.com/nuri428/langchain_opensearch.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9,<4',
)
