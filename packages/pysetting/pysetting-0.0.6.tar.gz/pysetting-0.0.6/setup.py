import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysetting",
    version="0.0.6",
    author="shivanandvp",
    author_email="shivanandvp.oss@gmail.com",
    description="A python library for parsing and storing settings and configurations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shivanandvp/pysetting",
    download_url="https://pypi.org/project/pysetting/",
    project_urls={
        'Documentation': 'https://github.com/shivanandvp/pysetting/',
        'Source': 'https://github.com/shivanandvp/pysetting',
        'Tracker': 'https://github.com/shivanandvp/pysetting/issues',
    },
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Typing :: Typed",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires='>=3.10'
)