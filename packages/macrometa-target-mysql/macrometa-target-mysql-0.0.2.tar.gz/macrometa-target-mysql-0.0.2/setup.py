# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macrometa_target_mysql', 'macrometa_target_mysql.tests']

package_data = \
{'': ['*'], 'macrometa_target_mysql.tests': ['data_files/*']}

install_requires = \
['c8connector==0.0.32',
 'cryptography>=41.0.2,<42.0.0',
 'prometheus-client==0.16.0',
 'pymysql>=1.1.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.30.0,<0.31.0']

entry_points = \
{'console_scripts': ['macrometa-target-mysql = '
                     'macrometa_target_mysql.target:MacrometaTargetMySQL.cli']}

setup_kwargs = {
    'name': 'macrometa-target-mysql',
    'version': '0.0.2',
    'description': 'A Meltano target for MySQL.',
    'long_description': '# target-mysql\n\n`target-mysql` is a Singer target for Oracle, Build with the [Meltano Target SDK](https://sdk.meltano.com).\n\n\n\nEnglish | [한국어](./docs/README_ko.md)\n\n\n## Installation\n\nUse PIP for installation:\n\n```bash\npip install thk-target-mysql\n```\n\nOr use GitHub Repo:\n\n```bash\npipx install git+https://github.com/thkwag/target-mysql.git@main\n```\n\n## Configuration\n\nThe available configuration options for `target-mysql` are:\n\n| Configuration Options   | Description                                | Default            |\n|-------------------------|--------------------------------------------|--------------------|\n| host                    | MySQL server\'s hostname or IP address      |                    |\n| port                    | Port where MySQL server is running         |                    |\n| user                    | MySQL username                             |                    |\n| password                | MySQL user\'s password                      |                    |\n| database                | MySQL database\'s name                      |                    |\n| table_name_pattern      | MySQL table name pattern                   | "${TABLE_NAME}"    |\n| lower_case_table_names  | Use lowercase for table names or not       | true               |\n| allow_column_alter      | Allow column alterations or not            | false              |\n| replace_null            | Replace null values with others or not     | false              |\n\nConfigurations can be stored in a JSON configuration file and specified using the `--config` flag with `target-mysql`.\n\n### The `replace_null` Option (Experimental)\n\nBy enabling the `replace_null` option, null values are replaced with \'empty\' equivalents based on their data type. Use with caution as it may alter data semantics.\n\nWhen `replace_null` is `true`, null values are replaced as follows:\n\n| JSON Schema Data Type | Null Value Replacement |\n|-----------------------|------------------------|\n| string                | Empty string(`""`)     |\n| number                | `0`                    |\n| object                | Empty object(`{}`)     |\n| array                 | Empty array(`[]`)      |\n| boolean               | `false`                |\n| null                  | null                   |\n\n\n## Usage\n\n```bash\ncat <input_stream> | target-mysql --config <config.json>\n```\n\n- `<input_stream>`: Input data stream\n- `<config.json>`: JSON configuration file\n\n`target-mysql` reads data from a Singer Tap and writes it to a MySQL database. Run Singer Tap to generate data before launching `target-mysql`.\n\nHere\'s an example of using Singer Tap with `target-mysql`:\n\n```bash\ntap-exchangeratesapi | target-mysql --config config.json\n```\n\nIn this case, `tap-exchangeratesapi` is a Singer Tap that generates exchange rate data. The data is passed to `target-mysql` through a pipe(`|`), and `target-mysql` writes it to a MySQL database. `config.json` contains `target-mysql` settings.\n\n## Developer Resources\n\n### Initializing the Development Environment\n\n```bash\npipx install poetry\npoetry install\n```\n\n### Creating and Running Tests\n\nCreate tests in the `macrometa_target_mysql/tests` subfolder and run:\n\n```bash\npoetry run pytest\n```\n\nUse `poetry run` to test `target-mysql` CLI interface:\n\n```bash\npoetry run target-mysql --help\n```\n\n### Testing with [Meltano](https://meltano.com/)\n\n_**Note:** This target functions within a Singer environment and does not require Meltano._\n\nFirstly, install Meltano and necessary plugins:\n\n```bash\n# Install Meltano\npipx install meltano\n\n# Initialize Meltano in this directory\ncd target-mysql\nmeltano install\n```\n\nThen, test and orchestrate with Meltano:\n\n```bash\n# Call tests:\nmeltano invoke target-mysql --version\n\n# Or execute pipeline with Carbon Intensity sample tap:\nmeltano run tap-carbon-intensity target-mysql\n```\n\n### SDK Development Guide\n\nFor in-depth instructions on crafting Singer Taps and Targets using Meltano Singer SDK, see the [Development Guide](https://sdk.meltano.com/en/latest/dev_guide.html).\n\n## Reference Links\n\n- [Meltano Target SDK Documentation](https://sdk.meltano.com)\n- [Singer Specification](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md)\n- [Meltano](https://meltano.com/)\n- [Singer.io](https://www.singer.io/)',
    'author': 'Macrometa',
    'author_email': 'info@macrometa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
