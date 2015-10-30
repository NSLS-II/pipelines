import setuptools
import versioneer

setuptools.setup(
    name='pipelines',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Eric Dill',
    author_email='edill@bnl.gov',
    description='Automagically generate analysis pipelines',
    url='http://github.com/NSLS-II/pipelines',
    platforms='Linux',
    license="BSD",
    packages=setuptools.find_packages(),
    package_data={'pipelines.nb': ['*.ipynb']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pipeline = pipelines.main:main',
        ],
    },
)
