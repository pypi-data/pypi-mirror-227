from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ProcessGuard',
    version='0.5.5',
    description='Python library for process management, monitoring, and guarding.',
    author='liad kaodsh',
    author_email='liad07@example.com',
    packages=find_packages(),
    install_requires=[
        'psutil',  # List your dependencies here
    ],
    long_description=long_description,  # Include the README content
    long_description_content_type="text/markdown",  # Specify the content type
    classifiers=[
        # ...
    ],
)
