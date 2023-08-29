# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wordpress_rss_archiver', 'wordpress_rss_archiver.utils']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.10,<7.0.0', 'requests>=2.30.0,<3.0.0']

entry_points = \
{'console_scripts': ['wordpress-rss-archiver = '
                     'wordpress_rss_archiver.wordpress_rss_archiver:main']}

setup_kwargs = {
    'name': 'wordpress-rss-archiver',
    'version': '0.1.0',
    'description': '',
    'long_description': '# wordpress-rss-archiver\n\n> WordPress.com/Automattic.com charges you US$38,000 to [host your blog for 100 years](https://wordpress.com/blog/2023/08/25/introducing-the-100-year-plan/) and automatically submit your site to the Internet Archive?  \n\nWell, We can do it for free... (the latter part at least, lol)\n\n## Installation\n\n```bash\npip install wordpress-rss-archiver\n```\n\n## Usage\n\n```bash\nwordpress-rss-archiver <feed_url> --ia-s3 <access_key:secret_key>\n```\n\nNOTE: register an Internet Archive account and get your access key and secret key from <https://archive.org/account/s3.php>\n',
    'author': 'yzqzss',
    'author_email': 'yzqzss@yandex.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
