import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kocoafab", # Replace with your own username
    py_modules=['ble_library','i2c_lcd','lcd_api','ssd1306','tcs34725'],
    version="0.0.8",
    author="kocoafab",
    author_email="kocoafab@kocoa.or.kr",
    description="Library to get readings from sensors on a ESP32.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://kocoafab.cc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)