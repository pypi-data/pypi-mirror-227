# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['profit']

package_data = \
{'': ['*']}

install_requires = \
['Pillow',
 'asyncio',
 'beautifulsoup4',
 'celery',
 'duckduckgo-search',
 'einops',
 'faiss-cpu',
 'ggl',
 'google-generativeai',
 'httpx',
 'langchain-experimental',
 'langchain==0.0.240',
 'nest_asyncio',
 'openai',
 'pegasusx',
 'playwright',
 'pydantic',
 'redis',
 'simpleaichat',
 'tenacity',
 'torch',
 'transformers',
 'wget']

setup_kwargs = {
    'name': 'profit-pilot',
    'version': '0.0.1',
    'description': 'ProfitPilot - AI Agents',
    'long_description': '# ProfitPilot\nProfitPilot is an autonomous AI sales professional agent.\n\n\n\n\n# Todo\n- Worker\n- Prompt,\n- Tools, Zapier tool, email answering, summarizng, email understanding, email response\n- Lead scraping, create tool that scrapes that scrapes on a website domain\n\n\n## Requirements\n- Email function tools\n- Zapier tools\n- Prompts\n- pdf tool',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/ProfitPilot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
