from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ez-video-convert",
    version="0.1",
    author="Malek Ibrahim",
    author_email="shmeek8@gmail.com",
    description="A simple tool to convert .mov video files to .mp4 format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ez-video-convert",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'click',
        'pyperclip',
    ],
    entry_points='''
        [console_scripts]
        mov2mp4=ez_video_convert.mov2mp4:convert_mov_to_mp4
    ''',
)