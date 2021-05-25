import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="MorshuTalk",
    version="0.0.1",
    author="n0spaces",
    description="Morshu text-to-speech",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/n0spaces/MorshuTalk",
    packages=["morshutalk", "morshutalkgui"],
    package_data={"morshutalk": ["morshu.wav"]},
    entry_points={
        "console_scripts": ["morshutalk=morshutalk.__main__:main", "morshutalkgui=morshutalkgui.__main__:main"],
    },
    install_requires=["g2p_en", "numpy", "pydub", "sounddevice"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
