from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='hephaestus-pro',
    version='1.0.0',
    description='Bloomberg-style Financial Intelligence Terminal powered by AI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ashraf Galib Shaik',
    url='https://github.com/AshrafGalibShaik/Hephaestus',
    license='MIT',
    packages=find_packages(include=['hephaestus']),
    install_requires=[
        'rich>=13.0.0',
        'plotext>=5.2.8',
        'pandas>=2.0.0',
        'python-dotenv>=1.0.0',
        'google-generativeai>=0.3.0',
        'openai>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'hephaestus=hephaestus.cli:main',
        ],
    },
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business :: Financial',
    ],
    keywords='finance terminal bloomberg cli dashboard ai revenue',
)
