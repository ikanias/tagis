# TAGIS - Trustification Automation of Generated Image SBOMs
A tool for automating images' SBOM files for analysis
--------------------------------------------------------------------------
This tool works under the Trustification project (https://github.com/trustification/trustification)
and the Exhort project (https://github.com/RHEcosystemAppEng/exhort)

How to use the tool?
---------------------

1. First clone the repository to your local machine: git clone git@github.com:ikanias/tagis.git
2. Copy the image location which you want to analyse to your clipboard. The image location can be long (i.e. quay.io/xiezhang7/hello-python:latest)
   or short (i.e. alpine:edge). Please do not add any prefix to the location like 'http://' or 'https://'
3. Run the tool by typing: python3 main.py
4. In the first prompt of the dialog insert or paste the image location which you want to analyse
5. In the second prompt insert the SBOM standard you want your SBOM to be generated in - cyclonedx or spdx
6. In the last prompt insert the file name you want for your SBOM. There is no need to add a suffix of file type, the file is automatically created as a .json file

During the SBOM being generated, you will see the purl of your image. This will be used later for sending the SBOM to Exhort for analysis using an API (i.e. with Postman). 
This purl will have to be sent with the generated SBOM in the same POST request to get the vulnerability analysis of the image.
