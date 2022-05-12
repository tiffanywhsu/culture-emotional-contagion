# Culture Emotional Contagion
Materials supporting "Social media in the U.S. and Japan: Cultural values shape the prevalence and contagiousness of affective content online" (Hsu et al., 2021, JPSP).

## Citation
Hsu, T.W., Niiya, Y., Thelwall, M., Ko, M., Knutson, B. and Tsai, J.L. (2021) Social media users produce more affect that supports cultural values, but are more influenced by affect that violates cultural values. Journal of Personality and Social Psychology. https://doi.org/10.1037/pspa0000282

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
