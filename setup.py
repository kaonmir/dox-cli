import setuptools


setuptools.setup(
    name="dox",
    version="0.0.1",
    license="MIT",
    author="kaonmir",
    author_email="sonjeff@naver.com",
    description="Make all DevOps experience better",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kaonmir/dox",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={"console_scripts": ["dox = dox.cli:cli"]},
)
