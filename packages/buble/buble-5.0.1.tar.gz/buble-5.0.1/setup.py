from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='buble',
  version='5.0.1',
  author='Forest_gleb',
  author_email='zykin_gleb@list.ru',
  description='Live buble',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/oftestyonety/dist_buble',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='buble if else elif elseif perimeter square area while for python',
  python_requires='>=3.7'
)
