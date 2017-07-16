from setuptools import setup
from endurance_model_obfuscator import __version__

setup(name='endurance_model_obfuscator',
      version=__version__,
      description="An Endurance SDK library for network model obfuscation.",
      url='http://www.gridwidgetlabs.com/products/endurance-sdk',
      author='Kevin D. Jones, Ph.D.',
      author_email='kevin.d.jones@gridwidgetlabs.com',
      license='MIT',
      install_requires=[
      ],
    #   entry_points={
    #     'console_scripts': [
    #         'endurance-admin=endurance.management.cli:main',
    #     ],
    # },
      zip_safe=False)
