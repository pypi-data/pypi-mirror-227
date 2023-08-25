from setuptools import setup
INSTALL_REQUIRES = [
    'np',
    'tk',
    'tk_tools',
    'customtkinter'
]
setup(
    name='RotaryTableDobotDidactech',
    packages=['RotaryTableDobotDidactech'],
    version='1.4',
    description='Rotary table for Dobot, DIDACTECH development',
    py_modules=['RotaryTableDobot'],
    author='Walter Becerra',
    author_email='becerrawalter20@hotmail.com',
    url=' ',
)