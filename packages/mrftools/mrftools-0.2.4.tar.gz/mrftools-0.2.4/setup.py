import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


with open("LICENSE", "r") as fh:
    license_text = fh.read()

setuptools.setup(
    name="mrftools",
    version="0.2.4",
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
        'numpy==1.25.2',
        'scipy==1.10.1',
        'h5py==3.7.0', 
        'matplotlib==3.5.1',
        'nibabel==4.0.2',
        'SimpleITK==2.2.0', 
        'torch==1.13.0', 
        'torchkbnufft>=1.4.1',
        'kornia==0.6.8', 
        'ismrmrd==1.12.3', 
        'fbpca==1.0', 
        'tqdm==4.62.3', 
        'jsonpickle==3.0.1', 
        'twixtools>=1.0'
    ],
    zip_safe=False, 
    license=license_text
)
