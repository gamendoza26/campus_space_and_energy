# Campus_Space_and_Energy



## Overview

This branch is set up to test files before moving them to origin main. It contains several directories:

1. **api:** Contains Dockerfiles, along with subdirectory "app" and "wifi-app"
2. **db:** Holds the scripts such that if we run the terminal, users can use the scripts without having access to the database
3. **jupyter:** Contains necessary files to generate heatmap visualization (html) through widgets
4. **website-front-end:** Contains all the images, resources and python files necessary to generate voila webpage

## Issues

1. **Merge conflicts:** Right now, we are struggling to fix merge conflicts. Jupyter creates new "execution_count" variables every time we render up the notebook through the voila window. This is annoying, but we have been able to work around it.

TEST