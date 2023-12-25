# What is MkDocs

MkDocs is a static site generator used to generate the documentation for `pyproxmox-ve`. We'll slowly get around to making a GitHub workflow to automatically generate these docs however when contributing to the project you must ensure the documentation is also maintained.

Here are some tips to do that.

## Running MkDocs locally

You can `pip install -r requirements-docs.txt` and then `pip install -e .` inside the `pyproxmox-ve` repository directory, the reason why you will need to install the package as editable is to reflect in real time any changes you are making to python classes/functions that are dynamically imported using `mkdocstrings-python`. Finally to serve the static pages locally for testing, run `mkdocs serve -a <ip>:<port>`. If you are developing locally on a machine and not remotely, then `mkdocs serve -a localhost:8001` is fine.

!!! note
    If you are using VSCode, ensure you install the `Code Spell Checker` extension to catch common spelling errors.

## Writing Documentation

Always try to be clear and concise when writing new documentation. If you are reading through the documentation and feel like something should be changed then feel free to make a pull request to correct the mistake. You should always reference the [MkDocs documentation](https://www.mkdocs.org/) and the [Material for MkDocs Reference Guide](https://squidfunk.github.io/mkdocs-material/reference/).

## pyproxmox-ve.github.io

GitHub Pages are used on the organization level so you can simply navigate to `pyproxmox-ve.github.io` instead of `pyproxmox-ve.github.io/docs`. If you haven't noticed while browsing the repository, you'll find the `docs/` folder is housed inside the `pyproxmox-ve` repository, so when building the documentation using the handy command line tool `mkdocs gh-deploy`, you need to clone both [pyproxmox-ve](https://github.com/pyproxmox-ve/pyproxmox-ve) and [pyproxmox-ve.github.io](https://github.com/pyproxmox-ve/pyproxmox-ve.github.io).

After both of these repositories have been cloned, ensure you are inside the `pyproxmox-ve-github.io` directory and use this command: `mkdocs gh-deploy --config-file ../pyproxmox-ve/mkdocs.yml --remote-branch main`. A simple GitHub workflow will be created in the future to clone both projects and perform this action on the staging/dev branch but for now it isn't an issue to do this manually.
