from setuptools import setup
INSTALL_REQUIRES = [
    'np',
    'matplotlib',
    'tk',
    'tk_tools',
    'customtkinter'
]
setup(
    name='RotaryTableDobotDidactech',
    packages=['RotaryTableDobotDidactech'],
    version='0.3',
    description='Rotary table for Dobot, DIDACTECH development',
    py_modules=['RotaryTableDobot'],
    author='Walter Becerra',
    author_email='becerrawalter20@hotmail.com',
    url=' ',
)