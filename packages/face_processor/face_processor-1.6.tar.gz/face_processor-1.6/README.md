# face-processor
 
Tool to process faces for psychophysics experiments. 

Adjust position of faces
make the images equiluminant

TODO: Describe module

Bainbridge, W. A., Isola, P., & Oliva, A. (2013). The Intrinsic Memorability of Face Photographs. Journal of Experimental Psychology: General, 142(4), 1323 - 1334.

# usage

## process distractors

This is done once to generate our distractor/control faces from the Bainsbridge database:

```python process_distractors.py```

## process probe

Place original photos in `stimuli/original/probes`. Crop the photo to leave a small margin around the top of the head, the ears and then chin. Then run (e.g.,):

```python process_probe.py ../original/probes/001.jpeg 1 M```