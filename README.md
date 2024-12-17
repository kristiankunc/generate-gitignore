# Generate Gitignore

A simple Python script to generate a .gitignore file for your project using the templates from [github.com/github/gitignore](https://github.com/github/gitignore)


## Templates

Templates are taken from the [github.com/github/gitignore](https://github.com/github/gitignore) repository and are updated every 24 hours.

The parsed list of templates can be found in the [templates.json](templates.json) file. This file is used by the script to generate the list of available templates.

I am not a maintainer of the gitignore source repository, so if you wish to have a template added, please open an issue or a pull request on the source repository as I do not maintain any custom templates.

## Usage

> [!WARNING]  
> Applying a template will overwrite any existing .gitignore file in the current directory, you will be prompted to confirm before proceeding.

Once installed, you can run the script with the following command:

```bash
generate-gitignore
```

### Listing all available templates

You can list all available templates with the list command:

```bash
generate-gitignore list
```

### Searching for a template

You can search for a template with the search command, it will launch an interactive search in the terminal allowing you to search by name and apply the selected template:

```bash
generate-gitignore search
```

### Generating a .gitignore file

If you want to apply a template directly, you can use the apply command followed by the template name:

```bash
generate-gitignore apply python
```

## Contributing

Contributions are welcome, please open an issue or a pull request if you wish to contribute. Make sure to follow the [Contribution Guidelines](CONTRIBUTING.md) before submitting a pull request.
