from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup_args = dict(
     name='ShynaBot',
     version='0.0.1',
     packages=find_packages(),
     author="Shivam Sharma",
     author_email="shivamsharma1913@gmail.com",
     description="Shyna Bot For App integration.BASIC META",
     long_description=long_description,
     long_description_content_type="text/markdown",
    )

install_requires = [
    "setuptools",
    "wheel",
    "wget",
    "chatterbot==1.0.4",
    "requests",
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
