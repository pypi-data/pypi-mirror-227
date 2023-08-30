from setuptools import setup, find_packages

setup(
    name='kanggenetools',
    version='0.7',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy'
    ],
    author='xiaowen kang',
    author_email='kangxiaowen@gmail.com',
    description='Tools for gene analysis by xiaowen kang',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/kanggenetools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
