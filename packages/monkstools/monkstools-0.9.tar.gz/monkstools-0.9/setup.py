from setuptools import setup, find_packages

setup(
    name='monkstools',
    version='0.9',  # version number
    packages=find_packages(),
    package_data={
        'monkstools': [
            'd1_data_map_customer_media.csv',
            'd2_data_map_perfer_product_customer.csv',
            'd3_data_map_delivery_cost_media.csv',
            'd4_data_map_product_costomerType.csv'
        ]
    },
    install_requires=[
        # e.g. 'numpy>=1.10'
    ],
    author='xiaowen kang',
    author_email='kangxiaowen@gmail.com',
    description='Tools for the Monks advertising platform',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/williampolicy/monkstools',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
