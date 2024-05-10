import cmd
import subprocess
import re
import time


class AutoOidc(cmd.Cmd):
    def generate_image_sbom(self, image, sbom_type, file_name):
        command = 'skopeo inspect docker://' + image + ' > digest_file.txt'
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        f = open("digest_file.txt", "r")
        lines = f.readlines()
        for line in lines:
            if line.find("Digest") != -1:
                a = line.strip(' :,"')
                b = a.lstrip('Digest":",')
                c = b.strip(' ",')
                d = c.replace('"', "")
                digest = d.replace(',', "")
                print(digest)
                break
        image_string = str(image)
        if '/' not in image_string:
            image_tag = image_string.split(":", 1)[1]
            product_name = image_string.split(":", 1)[0]
            image_without_tag = str(image_string.rsplit(':', 1)[0])
            print('Here is your purl: pkg:oci/' + product_name + '@' + digest + '?repository_url=' + image_without_tag + '&tag=' + image_tag)
        else:
            image_without_tag = str(image_string.rsplit(':', 1)[0])
            image_string.rsplit('/', 1)
            # Extract the image tag
            x = image_string.rsplit('/', 1)[1]
            product_name = x.split(":", 1)[0]
            image_tag = x.split(":", 1)[1]
            print('Here is your purl: pkg:oci/' + product_name + '@' + digest + '?repository_url=' + image_without_tag + '&tag=' + image_tag)
        # Install Syft if it does not exist
        command = 'which syft'
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = subprocess.check_output(['bash', '-c', command])
        if 'syft' not in str(output):
            print('You do not have syft installed in your machine. Installing Syft...')
            command = 'sudo curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin'
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = subprocess.check_output(['bash', '-c', command])
            print(output)
            time.sleep(30)
        if sbom_type == 'cyclonedx':
            command = 'syft ' + image + ' --scope all-layers -o cyclonedx-json -q > ' + file_name + '.json'
            print("generating your image cyclonedx SBOM file...")
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = subprocess.check_output(['bash', '-c', command])
            print(output)
            print('SBOM created successfully! The SBOM file for the image ' + image + ' has been created in your current folder as ' + file_name + '.json')
        elif sbom_type == 'spdx':
            command = 'syft ' + image + ' --scope all-layers -o spdx-json -q > ' + file_name + '.json'
            print("generating your image spdx SBOM file...")
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = subprocess.check_output(['bash', '-c', command])
            print(output)
            print('SBOM created successfully! The SBOM file for the image ' + image + ' has been created in your current folder as ' + file_name + '.json')
        elif (sbom_type != 'cyclonedx') or (sbom_type != 'spdx'):
            print("Your SBOM standard type is not of 'CycloneDX' or 'SPDX'. Please use only these standards")
            exit()
        elif sbom_type == '':
            print("You haven't set an SBOM standard type. Please set 'CycloneDX' or 'SPDX' as an SBOM standard")
            exit()


if __name__ == '__main__':
    print("***Welcome to Trustification image SBOM generator!***")
    image = input("Please enter the image location you want to analyse without the 'http:/https:' prefix: ")  # Enter \
    # the image location you want to generate an SBOM for - i.e. quay.io/xiezhang7/hello-python:latest
    sbom_type = input("Please enter the SBOM standard(cyclonedx/spdx): ")   # Enter the SBOM standard to be generated \
    # for the image - 'cyclonedx' or 'spdx'
    file_name = input("Please enter the name you want for your SBOM file: ")   # Enter your SBOM file name to use
    AutoOidc().generate_image_sbom(image, sbom_type, file_name)






