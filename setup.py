from setuptools import find_packages, setup

setup(
    name='bithumbpy',
    version='1.0',
    description='Bithumb open API python wrapper',
    url='https://github.com/inasie/bithumbpy',
    author='inasie',
    author_email='inasie@naver.com',
    license='MIT',
    install_requires=[
        'requests'
    ],
    packages=find_packages(),
    zip_safe=False
)
