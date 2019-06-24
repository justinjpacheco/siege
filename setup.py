from setuptools import setup

setup(name='siege',
      version='0.1',
      description='risk clone',
      url='https://github.com/justinjpacheco/siege',
      author='Justin Pacheco',
      author_email='justinjpacheco@gmail.com',
      license='BSD',
      packages=['siege'],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
        'flask',
        'simplekv',
        'pytest',
        'jsonschema',
      ],
      zip_safe=False)
