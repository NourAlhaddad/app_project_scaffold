from setuptools import setup, find_packages

setup(
    name="app_project_scaffold",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["create_project"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "scaffold=create_project:main",
        ],
    },
    author="Your Name",
    description="Generate project folders and files from a structure document",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/app_project_scaffold",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
