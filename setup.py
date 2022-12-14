import os
from setuptools import setup, find_packages

with open(os.path.join(".", "src", "muziq", "meta.py"), "r") as handle_meta:
    exec(handle_meta.read())


def dependencies(requirements_file):
    with open(requirements_file, "r") as handle:
        dependencies = handle.readlines()
        return [
            dependency
            for dependency in dependencies
            if len(dependency.strip()) > 0 and not dependency.strip().startswith("-e")
        ]


setup(
    name="muziq",
    version=VERSION,  # type: ignore
    description="A simple music utility to construct folder/ file style playlists for my 4Runner.",
    author="Usman Zubair",
    author_email="uzubair@gmail.com",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=dependencies("requirements.txt"),
    extras_require={"devel": dependencies("requirements-devel.txt")},
    python_requires=">=3",
    entry_points={"console_scripts": ["muziq=muziq.cmd:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
    ],
)
