from setuptools import setup

setup(
    name="seedance-2-api",
    version="0.1.0",
    author="Anil Matcha",
    description="A comprehensive Python wrapper for the Seedance 2.0 API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    py_modules=["seedance_api", "mcp_server"],
    install_requires=[
        "requests",
        "python-dotenv",
        "mcp[cli]"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
