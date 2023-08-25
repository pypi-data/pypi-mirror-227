import ai_calculator

dictionary_to_be_updated = {} #Este viene de la db

new_dict = ai_calculator.calculate_new_group_percentages(
  dictionary_to_be_updated,
  positive_variation=3,
  negative_variation=3,
  max_points=200,
  min_points=10)