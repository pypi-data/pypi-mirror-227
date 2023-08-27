# Octopype

## What is Octopype?

Octopype is a Wrapper for the [GitHub API](https://docs.github.com/rest) written in Python using the [requests](https://pypi.org/project/requests) library. \
The focus is on making it simple for the user and filling every niche with the features, that the GitHub API offers.

## Disclaimer

Octopype is still in Early Development and it does not have many features yet!

## Installing

```
pip install octopype
```

## Basic tutorials

### 1. Getting your Github bio.

```python
import octopype

github = octopype.OctoPype("INSERT TOKEN HERE")
print("My GitHub Bio is: " + github.account.info().bio)
```

### 2. Getting the name of a repository owner

```python
import octopype

github = octopype.OctoPype("INSERT TOKEN HERE")
print("The owner of Octopype's repository is: " + github.repository.getrepository("BLUEAMETHYST-Studios", "octopype").owner.name)
```

### 3. Updating your display name

```python
import octopype

github = octopype.OctoPype("INSERT TOKEN HERE")
github.account.update.display_name("OctoPype") # Will set your display name to 'OctoPype'
```

## License

[Octopype](https://github.com/BLUEAMETHYST-Studios/octopype) by [BLUEAMETHYST-Studios](https://github.com/BLUEAMETHYST-Studios) is licensed under the [GNU GENERAL PUBLIC LICENSE Version 3](https://gnu.org/licenses/gpl-3.0). \
To view the full license, click [here](https://github.com/BLUEAMETHYST-Studios/octopype/blob/main/LICENSE).