# BC Image Finder

Find your Neopet's [Beauty Contest](https://www.jellyneo.net/?go=beautycontest) images!

All Neopets trademarks belong to Neopets, I do not own Neopets. [Here](https://upload.neopets.com/robots.txt) is the robots.txt for the host of the BC images.

Shouldn't need to be said, but do not use art that you didn't draw yourself!

BC = Beauty Contest


### Instructions on use

1. Set petname to loop through (case-sensitive)

``PETNAME = "Poysion"``

2. Set the number of rounds your pet has won (if they won two trophies in a round, only one image is saved regardless)

``NUM_IMG_EXPECTED = 1``

3. Set how old your Neopet is (in hours)

``HOURS = 106272``


### Notes

* This doesn't tell you which colour trophy it won.

* NB: Your Neopet may have BC trophies from before its creation (i.e it was purged and then recreated afterwards)


### Requirements

* Python 3.11.7 (lower may also be fine)

* ``pip install httpx`` (for making HTTP requests asynchronously)