
from setuptools import find_packages, setup
import transformation

setup(
    name='opp-transformation',
    version=transformation.__version__,
    description='Open Permissions Platform Transformation Service',
    author='Open Permissions Platform Coalition',
    author_email='support@openpermissions.org',
    url='https://github.com/openpermissions/transformation-srv',
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts':
        ['open-permissions-platform-transformation-svr = transformation.app:main']}, requires=['tornado', 'koi']
)
