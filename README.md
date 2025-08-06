# Vancouver Restaurant Density Analysis Using OSM Data

In this project our main objective was to analyze spatial trends of chain vs independent restaurants across Vancouver using OpenStreetMap data. The goal was to visualize where each type of dining establishment tends to cluster and derive insights that could inform local residents, visitors, or city planners.

## Dataset Processing
- Source: OpenStreetMap (OSM) amenities dataset for Vancouver.
- Filtering: Focused on restaurant and fast-food venues; excluded cafes for relevance.
- Name Identification:
  - Combined web-scraped franchise lists with OSM "brand" tags.
  - Applied post-filtering to correct missed or mislabeled entries.

## Data Analysis 
- Visualization: Geolocated data points over a Vancouver map to detect visible clustering patterns.
- Chain vs. Non-Chain Comparison:
  - Chains: Fewer unique names, more branches, dense in commercial centers.
  - Non-chains: More unique names, fewer branches, distributed more evenly city-wide.

<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/974f4938-bddc-4d4a-8adf-79e35afc0386" />

## ML Models
- Gaussian Naive Bayes: Detected a concentration of franchises in Southeast Vancouver.
- K-Nearest Neighbors: Predicted franchise presence in urban cores, with non-chains dominating elsewhere.
- Random Forest: Provided the clearest spatial distinction, especially highlighting non-chain dominance in the Northwest region.

<img width="500" height="550" alt="Image" src="https://github.com/user-attachments/assets/ce471356-97b2-41fd-a32d-04533ae6d594" />

## Density Mapping & Visualization
- Scatterplots: Visualized precise restaurant locations on a scaled city map.

<img width="500" height="190" alt="Image" src="https://github.com/user-attachments/assets/29aa6411-97cb-4bd7-b117-7748e17b84b0" />

- Heatmaps: Showed density variations for both restaurant types, identifying Downtown as the highest-density region.

<img width="900" height="200" alt="Image" src="https://github.com/user-attachments/assets/63fed662-1317-4bd5-942f-b93bc21e633f" />

- ggplot & Plotnine: Used for density contour overlays.

<img width="1200" height="300" alt="Image" src="https://github.com/user-attachments/assets/1ff640ab-1a87-4920-a6c6-4927518b1232" />


## Project Challenges
- Data Inconsistencies: Difficulty in accurately labeling franchises (e.g., Cactus Club was misclassified).
- Definition Ambiguity: No universally accepted rule for what constitutes a "chain."
- Future Validity: Restaurant landscapes change; findings reflect a snapshot in time.

## Team Members
- Minjae Shin
- David Ligocki
- Dmitrii Beliaev
