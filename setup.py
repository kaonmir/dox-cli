import setuptools
from pathlib import Path


# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="dox-cli",
    version="0.0.9",  # TODO: 태그 걸면 배포되도록 수정
    license="MIT",
    author="kaonmir",
    author_email="sonjeff@naver.com",
    description="Make all DevOps experience better",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaonmir/dox-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={"console_scripts": ["dox = dox.cmd:cli"]},
)
