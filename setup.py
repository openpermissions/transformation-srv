
from setuptools import find_packages, setup
import transformation

setup(
    name='open permissions platform transformation service',
    version=transformation.__version__,
    description='Open Permissions Platform Transformation Service',
    author='CDE Catapult',
    author_email='support@openpermissions.org',
    url='https://github.com/openpermissions/transformation-srv',
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts':
        ['open-permissions-platform-transformation-svr = transformation.app:main']}, requires=['tornado', 'koi']
)
