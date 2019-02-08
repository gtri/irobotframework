# irobotframework

> _Interactive Acceptance Test-Driven Development and Robot Process Automation,
> powered by [IPython](http://ipython.org) and [Robot Framework](https://robotframework.org)_

irobotframework is a Jupyter Kernel that provides provides Robot Framework:

- test **execution** with **rich output** from Robot notebooks
  - ...and IPython with `%%robot`
- code **completion** and **inspection** in notebooks and consoles
- syntax **highlighting** in JupyterLab for notebooks and `.robot` and `.resource` files
- extensible Robot **magics**, **reporters**, and **completions**

Learn more in the documentation:

| Interactive                                                                                              | HTML                                                   | Notebooks                                                            | GitHub                                                             |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [Binder](https://mybinder.org/v2/gh/gtri/irobotframework/master?urlpath=lab%2Ftree%2Fdocs%2Findex.ipynb) | [readthedocs](https://irobotframework.readthedocs.org) | [nbviewer](https://github.com/gtri/irobotframework/docs/index.ipynb) | [GitHub](https://github.com/gtri/irobotframework/docs/index.ipynb) |

## Features

| Feature                                                                             | Screenshot                                      |
| ----------------------------------------------------------------------------------- | ----------------------------------------------- |
| _Launch Robot Framework as a Notebook, Console or edit Robot files_                 | [![][screenshot_launcher]][screenshot_launcher] |
| _Get rich completion of Robot language features, Libraries, Keywords and Variables_ | [![][screenshot_complete]][screenshot_complete] |
| _Inspect Libraries and Keywords... even ones you're writing_                        | [![][screenshot_inspect]][screenshot_inspect]   |
| _Work with Robot in IPython as an extension_                                        | [![][screenshot_magic]][screenshot_magic]       |
| _Use Console and Rich display_                                                      | [![][screenshot_console]][screenshot_console]   |

[screenshot_complete]: ./docs/_static/screenshots/screenshot_complete.png
[screenshot_console]: ./docs/_static/screenshots/screenshot_console.png
[screenshot_inspect]: ./docs/_static/screenshots/screenshot_inspect.png
[screenshot_launcher]: ./docs/_static/screenshots/screenshot_launcher.png
[screenshot_magic]: ./docs/_static/screenshots/screenshot_magic.png

## Install

```bash
# COMING SOON pip install irobotframework
# COMING SOON jupyter labextension install jupyterlab-irobotframework
```

or

```bash
# COMING SOON conda install -c conda-forge irobotframework jupyterlab-irobotframework
```

## Develop

Assuming a working [Anaconda](https://www.anaconda.com/download) or
[Miniconda](https://conda.io/miniconda.html):

```bash
conda install anaconda-project
anaconda-project run bootstrap
```

Now launch JupyterLab

```bash
anaconda-project run lab
```

Live develop by running the following in two prompts:

```bash
anaconda-project run jlpm watch
anaconda-project run lab --watch
```

> Note: Python changes require a kernel restart, TypeScript changes require a
> browser reload

## Free Software

`irobotframework` is developed on [GitHub](https://github.com/gtri/irobotframework)
and under the [BSD-3-Clause license](./LICENSE).
