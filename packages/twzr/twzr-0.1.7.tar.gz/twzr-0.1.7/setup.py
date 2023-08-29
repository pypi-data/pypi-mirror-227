import setuptools

setuptools.setup(
    name='twzr',
    version='0.1.7',
    author='Aspen Cage',
    author_email='aspenncage@gmail.com',
    description='Tweezer: teeny tiny tools for data processing',
    long_description="Microfunctions to help make pandas data transformation workflows faster. For example, Why type `df.filter(regex=re.compile('column',re.IGNORECASE))` when you can type `f(df,'column')`?",
    long_description_content_type="text/markdown",
    url='https://github.com/aspencage/twzr',
    download_url='https://github.com/aspencage/twzr/archive/refs/tags/v0.1.7.tar.gz',
    license='MIT',
    packages=['twzr'],
    install_requires=[
        'numpy',
        'pandas'
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10'
    ]
)