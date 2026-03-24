from setuptools import setup, find_packages

setup(
    name='hephaestus',
    version='1.0.0',
    description='Financial Intelligence Terminal powered by AI',
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
)
