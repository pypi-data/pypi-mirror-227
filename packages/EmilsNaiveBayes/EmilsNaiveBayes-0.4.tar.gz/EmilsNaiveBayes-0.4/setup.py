from distutils.core import setup

setup(
    name='EmilsNaiveBayes',  # How you named your package folder (MyLib)
    packages=['EmilsNaiveBayes'],  # Chose the same as "name"
    version='0.4',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Naive Bayes Algorithm implemented by me.',  # Give a short description about your library
    author='Emil Vinu',  # Type in your name
    author_email='emil.alexander.vinu@gmail.com',  # Type in your E-Mail
    url='https://github.com/SirPythonPhoenix/NaiveBayesPackage',
    # Provide either the link to your gitHub or to your website
    download_url='https://github.com/SirPythonPhoenix/NaiveBayesPackage/archive/refs/tags/v_0.4.tar.gz',
    # I explain this later on
    keywords=['Naive Bayes', 'Machine Learning'],  # Keywords that define your package best
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

)
