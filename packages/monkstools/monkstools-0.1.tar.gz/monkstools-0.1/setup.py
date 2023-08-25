from setuptools import setup, find_packages

setup(
    name='monkstools',
    version='0.1',  # ini
    packages=find_packages(),
    install_requires=[
        # e.g. 'numpy>=1.10'
    ],
    author='xiaowen kang',
    author_email='your.email@example.com',
    description='Tools for the Monks advertising platform',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/williampolicy/monkstools',  # 如果有的话
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
