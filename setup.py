from distutils.core import setup
setup(
    name = "autotester",
    packages = ["autotester"],
    version = "0.0.1",
    description = "Autonomous interactive tester control",
    author = "Igor Krawczuk",
    license="AGPLv3",
    author_email = "igor@krawczuk.eu",
    url = "https://github.com/wojcech/autotester",
    download_url = "https://github.com/wojcech/autotester/archive/master.zip",
    keywords = ["tester", "automated"],
    setup_requires = ["pytest-runner"],
    test_requirements = ['pytest','pytest-cov'],
    install_requires = [
    "pyvisa",
    "agilentpyvisa",
    "dataset",
    "pandas",
    "numpy"
    ],
    dependency_links=[ "git+https://github.com/wojcech/agilentpyvisa.git#egg=agilentpyvisa"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering",
        ],
    long_description = """\
Automated Charackterization of electrical components
-------------------------------------

Provides a collection of loosely coupled components in order to automate testing process with
automated agents.

Available for python3 only.
"""
)
