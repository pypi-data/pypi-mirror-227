from setuptools import setup, find_packages

with open("README.md", "r") as file:
	readme = file.read()

requirements = [
	"pyppeteer==1.0.2",
	"pyppeteer_stealth==2.7.4"
]

keywords = [
	"character",
	"characterai",
	"beta.character.ai",
	"c.ai",
	"kirbacter",
	"api"
]

setup(
	name="kirbacterai",
	version="0.0.3",
	author="KirbyRedius",
	long_description=readme,
	long_description_content_type="text/markdown",
	url="https://github.com/KirbyRedius/KirbacterAI",
	packages=find_packages(),
	install_requires=requirements,
	keywords=keywords,
	classifiers=[
		"Programming Language :: Python :: 3"
	]

)