"""Setup configuration for Finsight."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="finsight",
    version="0.1.0",
    author="Finsight Team",
    description="Financial institution connector framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khushwantraj/Finsight",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "plaid-python>=16.0.0",
        "kiteconnect>=4.2.0",
        "alpha-vantage>=2.3.1",
        "ccxt>=4.1.0",
        "celery>=5.3.4",
        "redis>=5.0.1",
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "cryptography>=41.0.7",
        "pyjwt>=2.8.0",
        "requests>=2.31.0",
        "httpx>=0.25.0",
        "sqlalchemy>=2.0.23",
        "alembic>=1.13.0",
        "psycopg2-binary>=2.9.9",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
        ],
    },
)
