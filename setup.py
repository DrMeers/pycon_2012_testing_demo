import setuptools

setuptools.setup(
    name='pycon-2012-testing-demo',
    version='0.1',
    description='PyCon AU 2012 Testing Demonstration',
    author='Simon Meers',
    author_email='simon@simonmeers.com',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',],
    install_requires=[],
    include_package_data=True
)
