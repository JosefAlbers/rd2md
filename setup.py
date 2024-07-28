from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = [l.strip() for l in f.readlines()]

setup(
    name="rd-to-md",
    url='https://github.com/JosefAlbers/rd2md',
    version="0.0.3",
    py_modules=["rd2md"],
    packages=find_packages(),
    readme="README.md",
    author_email="albersj66@gmail.com",
    description="Scrape reddit posts into a single markdown file",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Josef Albers",
    license="MIT",
    python_requires=">=3.12.3",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "rd2md=rd2md:main",
        ],
    },
)
