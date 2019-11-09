# ABPlayer Mini Helper
Python helper script that cuts audio books in smaller chunks for the ABPlayer hardware project.

More details about the hardware project [on Hackaday.io](https://hackaday.io/project/168330-abplayer-mini-audiobook-player).

## Description
The DFPlayer mini is great for playing short MP3 files. However, it doesn't have a way to move forwards or backwards on a track which makes it bad for audio books that are usually very long. 

My solution to this is to have a script that would cut up the audiobook into smaller chunks so that the DFPlayer can jump to each one as if it's moving forwards and backwards. The script needs to be smart enough to cut only on places where there is silence. This way the transitions between chunk/tracks would not be noticeable.
