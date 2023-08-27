# How to use new dataset

1. git clone https://github.com/circles-zone/gender-detection-local-python-package (All further commands are from perspective of root directory in git repo)
2. Copy a "Train", "Test", and "Validation" directory full of images with a "Male" and "Female" subdirectory in each (containing preferrably 178x218 images to ./CirclesGenderDetectionPython.
3. python3 ./CirclesGenderDetectionPython/UpdateModel.py
4. git add "gender_detection"
5. Make sure The training directories were not added to the new commit
6. Increment version number in setup.py
7. git commit
8. git push
