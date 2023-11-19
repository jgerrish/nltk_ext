from setuptools import setup, find_packages

setup(
    name="nltk_ext",
    version="0.1",
    # Package structure
    #
    # find_packages searches through a set of directories
    # looking for packages
    packages=find_packages(
        ".", exclude=["ez_setup", "*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    # package_dir directive maps package names to directories.
    # package_name:package_directory
    package_dir={"": "."},
    # Not all packages are capable of running in compressed form,
    # because they may expect to be able to access either source
    # code or data files as normal operating system files.
    zip_safe=True,
    # Entry points
    #
    # install the executable
    # entry_points = {
    #    'console_scripts': ['helloworld = greatings.helloworld:main']
    # },
    # Dependencies
    #
    # Dependency expressions have a package name on the left-hand
    # side, a version on the right-hand side, and a comparison
    # operator between them, e.g. == exact version, >= this version
    # or higher
    install_requires=[
        "",
    ],
    # Tests
    #
    # Tests must be wrapped in a unittest test suite by either a
    # function, a TestCase class or method, or a module or package
    # containing TestCase classes. If the named suite is a package,
    # any submodules and subpackages are recursively added to the
    # overall test suite.
    test_suite="nltk_ext.tests.suite",
    # Download dependencies in the current directory
    # tests_require = 'docutils >= 0.6',
    # Meta information
    #
    author="Joshua Gerrish",
    author_email="jgerrish@gmail.com",
    description="A set of extension packages to NLTK",
    url="http://www.joshuagerrish.com",
)
