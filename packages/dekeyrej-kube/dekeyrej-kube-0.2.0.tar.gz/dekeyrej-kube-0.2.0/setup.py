from setuptools import find_packages, setup

setup(
    name='kube',
    packages=find_packages(include=['kube']),
    version='0.2.0',
    description='Kubernetes secret CRUD routines',
    author='J.DeKeyrel',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)