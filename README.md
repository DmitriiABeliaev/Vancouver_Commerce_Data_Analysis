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

## ML Models
- Gaussian Naive Bayes: Detected a concentration of franchises in Southeast Vancouver.
- K-Nearest Neighbors: Predicted franchise presence in urban cores, with non-chains dominating elsewhere.
- Random Forest: Provided the clearest spatial distinction, especially highlighting non-chain dominance in the Northwest region.

## Density Mapping & Visualization
- Scatterplots: Visualized precise restaurant locations on a scaled city map.
- Heatmaps: Showed density variations for both restaurant types, identifying Downtown as the highest-density region.
- ggplot & Plotnine: Used for density contour overlays.
- Folium: For interactive map visualizations.
- Case Study: McDonald's locations highlighted as an example of a dominant chain.

## Project Challenges
- Data Inconsistencies: Difficulty in accurately labeling franchises (e.g., Cactus Club was misclassified).
- Definition Ambiguity: No universally accepted rule for what constitutes a "chain."
- Future Validity: Restaurant landscapes change; findings reflect a snapshot in time.

## Team Members
- Minjae Shin
- David Ligocki
- Dmitrii Beliaev
