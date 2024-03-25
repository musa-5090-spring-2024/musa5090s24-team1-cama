# Guidelines for Committing Code

## Clone the Repo
To commits to this repo, start by cloning a local copy using `git clone https://github.com/musa-5090-spring-2024/musa5090s24-team1-cama.git`.

## Make Commits to a New Branch
All changes should be added to the repo with reference to a specific issue or subject that you're addressing (i.e., a new UI component or a particular part of the ETL process). Create a new branch using `git checkout -b [lastname/branch-name]`, add changes using `git add [name of changed file(s)]`, commit them with `git commit -m '[a descriptive message]'`, and then push them to the repo with `git push`. Note that branch names should be formatted as `<github-username>/<issue-number>-<kebab-case-description>`. For example `vimusds/1069-fix-territory-on-mobile`. 

## Merge Branches to `main` via PR
Once you've pushed changes up to the repo, open a pull request on GitHub. Make sure to add a description of what the PR addresses, with specific reference to any relevant issues (close the relevant issues if appropriate). Then merge the PR, resolving any merge conflicts first if necessary.