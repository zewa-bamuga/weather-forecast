import os.path

__version__ = "0.0.9"
__project_name__ = "Fastapi Template Project with React Admin"
__root_dir__ = os.path.dirname(os.path.abspath(__file__))
__api_description__ = """
## Service Logic

TODO: WIP
"""
__changelog__ = open(os.path.join(__root_dir__, "../CHANGELOG.md")).read()[:1000]
__api_description__ += (
    """
## Changelog
"""
    + __changelog__
    + """

> See full changelog in repository "src" dir
"""
)
