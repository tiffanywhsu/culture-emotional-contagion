# Culture Emotional Contagion
Materials supporting "Cultural ideals modulate affective content and contagion on social media" (Hsu et al., submitted).

## Citation
[insert citation]

## Content
### Data
Data were collected through the public Twitter API (https://dev.twitter.com/overview/api). To comply with the Twitter Developer Agreement and Policy, data cannot be publicly shared. Interested researchers may reproduce the experiments by following the procedure described in the paper. Anonymized data may be available upon reasonable request from Tiffany W. Hsu (twhsu@stanford.edu).

### Code
The preprocessing scripts should be used in the following order:
- Collect Twitter data using twitter_collection.py
- Obtain English SentiStrength (http://sentistrength.wlv.ac.uk/) and Japanese SentiStrength (https://github.com/tiffanywhsu/japanese-sentistrength)
- run_en_sentistrength.py (for using English SentiStrength) | run_jp_sentistrength.py (for using Japanese SentiStrength)
- process_sentistrength_results.py
- calculate_exposure.py
- aggregate_across_samples.py

To analyze data, first run preprocess_for_affective_content.py and preprocess_for_affective_contagion.py, then use the files outputted in analyze.Rmd.


## Authors
- **Tiffany W. Hsu** (PhD candidate, Stanford University) -- for writing the majority of the code, developing the contagion model
- **Michael Ko** (Masters student, Stanford University) -- for optimizing calculate_exposure.py


## Acknowledgements
- **Mike Thelwall** (Professor, University of Wolverhampton, UK) -- for contributing to Japanese SentiStrength and for developing English SentiStrength
- **Yu Niiya** (Professor, Hosei University, Japan) -- for contributing to Japanese SentiStrength

