from setuptools import find_packages, setup

PACKAGE_NAME = "content_safety_text"

setup(
    name=PACKAGE_NAME,
    version="0.0.4",
    description="This is my tools package",
    packages=find_packages(),
    entry_points={
        "package_tools": ["content_safety_text_tool = content_safety_text.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)