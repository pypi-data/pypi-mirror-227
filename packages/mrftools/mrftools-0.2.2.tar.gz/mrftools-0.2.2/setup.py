import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


with open("LICENSE", "r") as fh:
    license_text = fh.read()

setuptools.setup(
    name="mrftools",
    version="0.2.2",
    author="Andrew Dupuis",
    author_email="andrew.dupuis@case.edu",
    description="Tools for Magnetic Resonance Fingerprinting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.casemri.com/common-resources/mrftools",
    package_dir = {'': 'src'}, # Our packages live under src but src is not a package itself
    packages=setuptools.find_packages("src"), exclude=["test"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy==1.20.0',
        'scipy',
        'h5py', 
        'matplotlib',
        'nibabel',
        'SimpleITK', 
        'torch', 
        'torchkbnufft',
        'kornia', 
        'ismrmrd', 
        'fbpca', 
        'tqdm', 
        'jsonpickle'
    ],
    zip_safe=False, 
    license=license_text
)
