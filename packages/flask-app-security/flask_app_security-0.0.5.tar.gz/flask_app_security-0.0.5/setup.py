import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "flask_app_security",
    version = "0.0.5",
    author = "William Burriss",
    author_email = "williamb03@vt.edu",
    description = "Provides utilities for securing passwords and handling user sessions.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/williamburriss/flask_app_security/tree/main",
    project_urls = {
        "Report bugs": "https://github.com/williamburriss/flask_app_security/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
    install_requires=['joserfc>=0.7.0'],
)