from setuptools import setup, find_packages
setup(
    name='astrie',                # Package name
    packages=find_packages(),     # List of packages to include
    version='1.1',                # Version of your package
    license='MIT',                # License type
    author='Ashish Yadav',        # Author name
    author_email='unixm98@gmail.com',  # Author email
    description='A simple trie data structure implementation',  # Short description
    long_description='A comprehensive trie data structure implementation ...',  # Detailed description
    long_description_content_type='text/markdown',  # Type of long description content
    keywords=['trie', 'astrie', 'data structures', 'trie data structure'],  # Keywords
    url = 'https://github.com/ashishyadav2/astrie',   # Provide either the link to your github or to your website
    classifiers=[  # Metadata and classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
)
