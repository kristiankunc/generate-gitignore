# Generate Gitignore

A simple Python script to generate a .gitignore file for your project using the templates from [github.com/github/gitignore](https://github.com/github/gitignore)

[![Pip install](https://img.shields.io/badge/pip_install-generate--gitignore-blue)](https://pypi.org/project/generate-gitignore/)
[![PyPI - Version](https://img.shields.io/pypi/v/generate-gitignore)](https://pypi.org/project/generate-gitignore/#history)

[![Build a Publish](https://github.com/kristiankunc/generate-gitignore/actions/workflows/build-and-publish.yml/badge.svg?event=release)](https://github.com/kristiankunc/generate-gitignore/actions/workflows/build-and-publish.yml)
[![Update Templates](https://github.com/kristiankunc/generate-gitignore/actions/workflows/update-templates.yaml/badge.svg?event=schedule)](https://github.com/kristiankunc/generate-gitignore/actions/workflows/update-templates.yaml)

## Templates

Templates are taken from the [github.com/github/gitignore](https://github.com/github/gitignore) repository and are updated every 24 hours.

The parsed list of templates can be found in the [templates.json](templates.json) file. This file is used by the script to generate the list of available templates.

I am not a maintainer of the gitignore source repository, so if you wish to have a template added, please open an issue or a pull request on the source repository as I do not maintain any custom templates.

## Usage

### Installation

Install the package using pip:

```bash
pip install generate-gitignore
```

### Running

Once installed, you can run the script with the following command:

```bash
generate-gitignore
```

#### Listing all available templates

You can list all available templates with the list command:

```bash
generate-gitignore list
```

#### Searching for a template

You can search for a template with the search command, it will launch an interactive search in the terminal allowing you to search by name and apply the selected template:

```bash
generate-gitignore search
```

#### Generating a .gitignore file

If you want to use a template directly, you can use the use command followed by an array of template names:

```bash
generate-gitignore use python visualstudiocode ...
```

## Contributing

Contributions are welcome, please open an issue or a pull request if you wish to contribute. Make sure to follow the [Contribution Guidelines](CONTRIBUTING.md) before submitting a pull request.
