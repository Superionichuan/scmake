from setuptools import setup, find_packages

setup(
    name='scmake',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',  # 您的代码依赖的库
    ],
    entry_points={
        'console_scripts': [
            'scmake = scmake.expand_poscar:main',  # 将 scmake 命令行与 main 函数绑定
        ],
    },
    author='Sun Shichuan',
    author_email='shichuan.sun@ntu.edu.sg',
    description='A tool for expanding POSCAR files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Superionichuan/scmake',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

