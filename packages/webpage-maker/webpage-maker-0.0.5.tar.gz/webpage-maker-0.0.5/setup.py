import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="webpage-maker",
  version="0.0.5",
  author="Chenfan Wang",
  author_email="admin@wcfstudio.cn",
  description="A Python library for generating (rendering) static HTML web pages",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitee.com/wang-chenfan/webpage-maker",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)