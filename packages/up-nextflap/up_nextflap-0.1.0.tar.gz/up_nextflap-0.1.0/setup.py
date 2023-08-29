import platform
from setuptools import setup

long_description=\
"""============================================================
    UP_NEXTFLAP
 ============================================================
"""

arch = (platform.system(), platform.machine())

EXECUTABLES = {
    ("Linux", "x86_64"): ['libz3.so', 'nextflap.so'],
    ("Windows", "x86_64"): ['libz3.dll', 'nextflap.pyd'],
    ("Windows", "AMD64"): ['libz3.dll', 'nextflap.pyd'],
}

executable = EXECUTABLES[arch]

setup(
    name='up_nextflap',
    version='0.1.0',
    description='up_nextflap',
    long_description=long_description,
    long_description_content_type ="text/markdown",
    author='Oscar Sapena',
    author_email='ossaver@upv.es',
    url = "https://github.com/aiplan4eu/up-nextflap",
    packages=['up_nextflap'],
    data_files=[('.', executable)],
    install_requires=[
        'numpy', 'unified-planning'
    ],
    include_package_data=True,
)