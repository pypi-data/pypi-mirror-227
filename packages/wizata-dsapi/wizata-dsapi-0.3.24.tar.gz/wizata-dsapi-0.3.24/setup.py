from setuptools import setup

setup(
    name='wizata-dsapi',
    version='0.3.24',
    description='Wizata Data Science Toolkit',
    author='Wizata S.A.',
    author_email='info@wizata.com',
    packages=['wizata_dsapi'],
    install_requires=[
        'dill==0.3.6',
        'pandas==1.5.3',
        'numpy==1.23.5',
        'matplotlib==3.7.1',
        'protobuf==3.19.6',
        "tensorflow==2.7; sys_platform != 'darwin' or platform_machine != 'arm64'",
        "tensorflow-macos==2.11.0; sys_platform == 'darwin' and platform_machine == 'arm64'",
        "keras==2.7; sys_platform != 'darwin' or platform_machine != 'arm64'",
        "keras==2.11.0; sys_platform == 'darwin' and platform_machine == 'arm64'",
        'tensorflow_probability==0.15.0',
        'scikit-learn==1.2.2',
        'plotly==5.13.1',
        'adtk==0.6.2',
        'scipy==1.10.1',
        'xgboost==1.7.4',
        'joblib==1.2.0',
        'requests==2.28.2',
        'setuptools==67.6.0',
        'explainerdashboard==0.4.2.1',
        'ipywidgets==8.0.4',
        'kaleido==0.2.1',
        'pytest==7.2.2',
        'pytest-cov==4.0.0',
        'shapely==2.0.1',
        'pyodbc==4.0.35',
        'msal==1.21.0',
        'darts==0.25.0',
        'optuna==3.3.0'
    ]
)
