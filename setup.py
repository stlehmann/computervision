from setuptools import setup

setup(
    name='computervision',
    version='0.1.0',
    packages=['computervision'],
    package_dir={'': 'src'},
    scripts=["scripts/motion-detection_mog2.py", "scripts/motion-capture.py"],
    url='',
    license='MIT',
    author='Stefan Lehmann',
    author_email='stlm@posteo.de',
    description='some computervision examples',
    install_requires=['imutils'],
)
