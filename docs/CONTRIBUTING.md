# Guidelines for Committing Code

## Clone the Repo
To commits to this repo, start by cloning a local copy using `git clone https://github.com/musa-5090-spring-2024/musa5090s24-team1-cama.git`.

## Make Commits to a New Branch
All changes should be added to the repo with reference to a specific issue or subject that you're addressing (i.e., a new UI component or a particular part of the ETL process). Create a new branch using `git checkout -b [lastname/branch-name]`, add changes using `git add [name of changed file(s)]`, commit them with `git commit -m '[a descriptive message]'`, and then push them to the repo with `git push`.

## Merge Branches to `main` via PR
Once you've pushed changes up to the repo, open a pull request on GitHub. Make sure to add a description of what the PR addresses, with specific reference to any relevant issues (close the relevant issues if appropriate). Then merge the PR, resolving any merge conflicts first if necessary.




If you would like to contribute to any part of the codebase, please fork the repository [following the Github forking methodology](https://docs.github.com/en/github/getting-started-with-github/quickstart/fork-a-repo). Make changes to the code in your own copy of the repository – including tests if applicable – and [submit a pull request against the upstream repo.](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) In order for us to merge a pull request, the following checks are enabled within this repo:

- Merges to `main` are prohibited - please open a pull request from a branch
- Please create a branch name in the format of `<github-username>`/`<issue-number>`-`<kebab-case-description>`. For example vimusds/1069-fix-territory-on-mobile
- At least one required reviewer must approve the commit (see [CODEOWNERS](https://github.com/CodeForPhilly/vacant-lots-proj/blob/main/.github/CODEOWNERS)) for the most up-to-date list of these members)
- All required status checks must pass

If there is significant dissent within the team, a meeting will be held to discuss a plan of action for the pull request.

#### Making code changes

Changes to our codebase should always address an [issue](https://github.com/CodeForPhilly/vacant-lots-proj/issues) and need to be requested to be merged by submitting a pull request that will be reviewed by at least the team lead or tech lead.

#### Choose an issue

Look through the [issues page](https://github.com/CodeForPhilly/vacant-lots-proj/issues) in the repo.

Find a task that has no current assignees and sounds like a task that either you can confidently take on yourself or involves a new language, framework, or design that you want learn.

For the latter it is best to pair on this with a team member experienced with that thing you want to learn. 

#### Commit your work

Any good work with code involves good commit messages.

The best commit messages read like instructions on how to recreate the code being committed.

Individual commits should be small chunks of work included together as one step in the process.

#### Push your work up to the remote repo

When you have completed your work and made good commit messages that read like clear instructions, you will want to push your work up to our remote repository on Github.

```sh
# Make a matching remote branch to push to
# Note: While it is usually `origin`, the remote repo may be named a different alias on your machine
git push --set-upstream origin <new-branch-name>

# Once you have set up a remote branch continue to push changes with:
git push
```

#### Create a pull request

In order to merge your work to the `develop` branch you must create a pull request.

Often Github will put up a notification that a new branch has been pushed and give a green "Make a PR" button on any page of the repo. If you don't see this you can go to the [pull requests tab](https://github.com/CodeForPhilly/vacant-lots-proj/pulls) and hit the big green `New` button.

There is a template to follow to make sure that reviewers have enough context about the changes you made and what they fix.

It is vital to provide clear instructions how to test the changes you made.

Please also make sure you tag the issue you are addressing. You can do this when writing the PR by writing `#<number>` in the `Does this close any currently open issues` section.

```md
<!-- For example, for a PR addressing issue #13 -->
Closes #13
```

To make sure reviewers know to review it, finish up by assigning either the team lead or two team members in the 'reviewers' tab in the sidebar or under the PR text depending on your view.

#### Reviewed work

The reviewer(s) will either ask for changes or approve the PR.

If changes are requested, please make the changes in your branch and push them up to Github when ready.

```bash
# Tip: If you are fixing something from a particular commit, you can create a !fixup commit with
git commit --fixup <sha-for-commit>

# Then, when approved, before you merge you can use:
git rebase -i --autosquash develop
# to squash your !fixup commits into their corresponding commits and make sure your branch is up to date with develop
```

Once you have pushed up your fixes, let your reviewer know and they will follow up and look again. This may loop a few times.

Once your changes are approved, you can hit the `merge` button to merge to the `develop` branch (unless specified otherwise).

Please also delete the branch from Github (you'll be prompted).

#### Update changelog

We keep a changelog following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format. In the unreleased section add the following line to one of the sections within unreleased:

```md

### Added

- Add your PR title [#1](https://github.com/CodeForPhilly/vacant-lots-proj/pull/1)

```

You would use your PR's title, the number of your PR, and the link to that PR. There are a few sections: `Added, Changed, Deprecated, Removed, Fixed, Security`, and you should add your line to the section that best matches what your PR is contributing.

#### Clean up

Once you've merged your work go back to your terminal

```sh
# Go to the develop branch
git checkout develop

# Pull down the changes you merged
git pull

# Delete the branch from your local machine
git branch -d <new-branch-name>
```

