# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarm_logic',
 'swarm_logic.connectors',
 'swarm_logic.experimental',
 'swarm_logic.utils']

package_data = \
{'': ['*']}

install_requires = \
['fastapi', 'swarms']

setup_kwargs = {
    'name': 'swarmlogic',
    'version': '0.6.4',
    'description': 'SwarmLogic - Pytorch',
    'long_description': '# SwarmLogic: Your Fluid AI-Powered Backend \n\nSwarmLogic is an innovative backend solution leveraging swarm intelligence and powered by advanced AI models. It evolves based on API calls, automatically inferring business logic and managing data persistence, saving you from the complexities of traditional backend development.\n\n## Objective\n\nSwarmLogic aims to revolutionize backend development by reducing complexity, saving time, and increasing efficiency. We aim to create a system where backends can evolve based on API calls, automatically inferring business logic, and managing data persistence.\n\n## Architecture\n\nSwarmLogic follows a unique architecture inspired by swarm intelligence. At its core, SwarmLogic utilizes an array of AI agents, each capable of learning and adapting from every API call.\n\n* API Calls: The starting point of our architecture. Any API call triggers our AI swarm.\n* AI Swarm: A group of AI agents that interpret the API calls, infer the business logic, and handle the data state.\n* Business Logic Inference: Our AI agents use natural language understanding and processing capabilities to understand the purpose of the API call and derive the business logic.\n* Data State Management: SwarmLogic automatically manages the data state based on the inferred business logic. It can handle data persistence for different schemas and data sources.\n\n## Getting Started\n\n### Prerequisites\n\n- Python 3.7 or above\n- FastAPI\n- An OpenAI API key\n\n### Installation\n\nClone the repository by running the following command in your terminal:\n\n```bash\ngit clone https://github.com/kyegomez/SwarmLogic.git\n```\n\nOnce cloned, navigate to the `SwarmLogic` directory:\n\n```bash\ncd SwarmLogic\n```\n\nInstall the required Python packages:\n\n```bash\npip install -r requirements.txt\n```\n\n## Usage\n\nTo start the server, run the following command in the terminal:\n\n```bash\nuvicorn main:app --reload\n```\n\nThe FastAPI server will start and you can interact with the backend via `http://localhost:8000`.\n\nFor API calls, make a POST request to `http://localhost:8000/{app_name}/{api_call}` with a JSON body.\n\n### Example\n\n```bash\ncurl -X POST "http://localhost:8000/todo_list/create_todo" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\\"app_name\\":\\"todo_list\\",\\"api_call\\":\\"create_todo\\"}"\n```\n\nIn case of an error or exception, check the `app.log` file in the root directory for detailed information.\n\n## Contributing\n\nWe appreciate contributions of any kind and acknowledge them on our README. Please follow the existing coding style, use descriptive commit messages, and remember to test your contributions before submitting a pull request.\n\n## Roadmap\n\nWe\'re dedicated to innovating backend development, and our roadmap is a testament to that. Each phase is a calculated step towards making our vision a reality. To learn more, check out the [roadmap file](docs/ROADMAP.md) file in the root directory.\n\n## License\n\nThis project is licensed under the terms of the MIT license. See `LICENSE` for additional details.\n\n## Acknowledgments\n\nA big thank you to our team of researchers, software engineers, and technology enthusiasts committed to innovating and revolutionizing how backends are built. Your hard work is appreciated!\n\nHappy coding!\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/SwarmLogic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
