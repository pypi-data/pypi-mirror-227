import setuptools

# get __version__
exec( open( 'automatic_cv/_version.py' ).read() )

with open("README.md", "r") as fh:
    long_description = fh.read()

project_urls = {
    'Source Code': 'https://github.com/DangerLin/Automatic-CV',
    'Bug Tracker': 'https://github.com/DangerLin/Automatic-CV/issues'
}

setuptools.setup(
    name = "Automatic-CV",
    version = __version__,
    author = "Danger Lin",
    author_email = "dangerlin100@gmail.com",
    description = "Control the Biologic potentiostat to test CV experiment via Python (combination with OT-2)",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = [ 'biologic' ],
    url = "",
    project_urls = project_urls,
    packages = setuptools.find_packages(),
    python_requires = '>=3.7',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 3 - Alpha"
    ],
    install_requires = [],
    package_data = {
        'automatic_cv': [
            'techniques_version.json',
            f'techniques-*/*'
        ]
    }
)
