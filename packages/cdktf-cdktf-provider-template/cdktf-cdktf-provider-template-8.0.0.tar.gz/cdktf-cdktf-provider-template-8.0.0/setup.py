import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-template",
    "version": "8.0.0",
    "description": "Prebuilt template Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-template.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-template.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_template",
        "cdktf_cdktf_provider_template._jsii",
        "cdktf_cdktf_provider_template.cloudinit_config",
        "cdktf_cdktf_provider_template.data_template_cloudinit_config",
        "cdktf_cdktf_provider_template.data_template_file",
        "cdktf_cdktf_provider_template.dir",
        "cdktf_cdktf_provider_template.file",
        "cdktf_cdktf_provider_template.provider"
    ],
    "package_data": {
        "cdktf_cdktf_provider_template._jsii": [
            "provider-template@8.0.0.jsii.tgz"
        ],
        "cdktf_cdktf_provider_template": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdktf>=0.18.0, <0.19.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.87.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
