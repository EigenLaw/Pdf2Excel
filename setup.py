import re
import io
from setuptools import setup
from setuptools.extension import Extension


setup(
    author="Eigen",
    author_email="eigenluo@gmail.com",
    name='Pdf2Excel',
    version="1",
    url='https://github.com/EigenLaw/Pdf2Excel',
    description='Turn pdf into excel file using ABBYY API',
    license='MIT',
    install_requires=['numpy>=1.6.1'],#'time', 'argparse', 'AbbyyOnlineSdk'
    #ext_modules=[Extension("wordcloud.query_integral_image",
    #                       ["wordcloud/query_integral_image.c"])],
    scripts=['Pdf2Excel.py'],
    #packages=['Pdf2Excel'],
    #package_data={'wordcloud': ['stopwords', 'DroidSansMono.ttf']}
)
