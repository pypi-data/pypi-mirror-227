"""
https://packaging.python.org/en/latest/tutorials/packaging-projects/
Markdown: https://www.markdownguide.org/cheat-sheet/
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Latestearthquake-Indonesia_byTaufik",
    version="0.1",
    author="Taufik Budi Santosa",
    author_email="taufikbudis@gmail.com",
    description="The package will get the latest earthquake from BMKG | Meteorological, Climatological, and"
                "Geophysical Agency",
    long_description=long_description,
    long_description_content_text="text/markdown",
    url="https://github.com/Zerex-Id/latest-indonesia-eartquake",
    project_urls={
        "Website": "https://github.com/orgs/Zerex-Id/repositories",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    # python_requires=">=3.11",
    packages=setuptools.find_packages(),
    python_requires=">=3.11",
)
