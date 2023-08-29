from setuptools import setup, find_packages

setup(
    name='anodot-monitor',
    version="0.2",
    description='Anodot Monitoring for Python',
    author='Alexander Shereshevsky',
    author_email='ashereshevsky@anodot.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
      line.strip() for line in open("requirments.txt").readlines()
    ],
    entry_points={
      "console_scripts": [
          "anodot-cli=example:main"
      ]
    },
)
