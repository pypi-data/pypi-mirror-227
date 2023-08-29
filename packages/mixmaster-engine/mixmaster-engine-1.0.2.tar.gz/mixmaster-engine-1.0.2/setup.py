from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='mixmaster-engine',
      version='1.0.2',
      license='MIT License',
      author='Gabriel Fernandes',
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email='g.silvafdc@gmail.com',
      keywords='mixmaster',
      description=u'Engine para banco de dados do MixMaster',
      python_requires='>=3.9',
      packages=[
          'MixMasterEngine',
          'MixMasterEngine/app',
          'MixMasterEngine/app/gamedata',
          'MixMasterEngine/app/LogDB',
          'MixMasterEngine/app/Member',
          'MixMasterEngine/app/Profile',
          'MixMasterEngine/app/S_Data',
          'MixMasterEngine/app/Web_Account'],
      url='https://github.com/gsfcosta/mixmaster-engine',
      install_requires=['SQLAlchemy', 'dynaconf', 'DateTime'],)
