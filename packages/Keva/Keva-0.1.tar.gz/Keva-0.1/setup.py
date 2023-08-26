from setuptools import setup


setup(
    name='Keva',
    version='0.1',
    license='MIT',
    description= "A python client for the Keva Database",
    long_description= open("README.md").read(),
    long_description_content_type= "text/markdown",
    project_urls={"Homepage": "https://keva.pancakedev.repl.co"},
    author="gugu256",
    author_email='gugu256@mail.com',
    url='https://github.com/gugu256/gugu256',
    keywords='database key value key-value KV',
    install_requires=[
          'requests',
      ],
    classifiers= [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]

)

