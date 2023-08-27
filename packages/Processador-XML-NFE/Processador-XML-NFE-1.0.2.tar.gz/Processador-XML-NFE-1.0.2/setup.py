from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='Processador-XML-NFE',
      version='1.0.2',
      license='MIT License',
      author='Henrique Venancio',
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email='hvs.git@gmail.com',
      keywords='NFE',
      description=u'Extraia relatórios a partir do XML de diversas Notas Fiscais Eletrônicas(NFE) e ('
                  u'NFCE) de uma só vez!',
      packages=['processador_nfe'],
      install_requires=['pandas', 'openpyxl'], )
