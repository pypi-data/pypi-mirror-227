from setuptools import setup, find_packages

README_FILE = 'README.md'

project_name = "cola-ml"
setup(
    name=project_name,
    description="",
    version="0.0.1",
    author="Marc Finzi and Andres Potapczynski",
    author_email="maf820@nyu.edu",
    license='MIT',
    python_requires='>=3.10',
    install_requires=[
        'scipy', 'tqdm>=4.38',
        'cola-plum-dispatch==0.1.1',
    ],
    extras_require={
        'dev': ['pytest', 'pytest-cov'],
    },
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wilson-labs/cola',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords=[
        'linear algebra',
        'linear ops',
        'sparse',
        'PDE',
        'AI',
        'ML',
    ],
)
