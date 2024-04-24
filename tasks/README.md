# Info for the Tasks Subdirectory

This subdirectory in the monorepo uses Python to ETL data and load it to Google Cloud for visualization in the UI. Setup instructions are in [the `SETUP.md`](/docs/SETUP.md). Further info is below.

## Adding Packages
This subdirectory uses `poetry` for package management. If you need to add a package, you can do this by running `poetry add [package name]`. There is a pre-commit hook set up to automatically add new packages to the `requirements.txt` file when you push to GitHub.

## Autoformatting
We're using [`black` to autoformat code](https://github.com/psf/black) according to a consistent standard. Again, there's a pre-commit hook set up to do this when you push to GitHub. In the event that `black` reformats some of your code, you'll have to re-add the relevant code to your commit using `git add *` and then a commit message like `git commit -m 'add reformatted code'`. 

## Using the .venv as a kernel
If you want to run code in a Jupyter notebook, you can use the `poetry` environment associated with the repository. Simply look for the kernel called `.venv` when VS Code asks you which kernel you'd like to select.
