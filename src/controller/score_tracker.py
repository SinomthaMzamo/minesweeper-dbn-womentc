import csv


#  demo
with open('data.csv', 'w', newline='') as csvfile:
  # Your code to write data to the file
  pass


writer = csv.writer(csvfile)
# todo writerow(): This method writes a single row of data to the CSV file.
#  Each element in the row should be a separate item.
data_row = ["Name", "Age", "City"]
writer.writerow(data_row)


# todo: writerows(): This method writes multiple rows of data to the CSV file.
#  It takes a list of lists, where each inner list represents a single row.
data = [
  ["Alice", 30, "New York"],
  ["Bob", 25, "Los Angeles"],
  ["Charlie", 40, "Chicago"]
]
writer.writerows(data)


import csv

data = [
  ["Name", "Age", "City"],
  ["Alice", 30, "New York"],
  ["Bob", 25, "Los Angeles"],
  ["Charlie", 40, "Chicago"]
]

with open('data.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(data)

print("Data written to CSV file!")


# todo example
import csv

MAX_SCORES = 10  # Define the maximum number of high scores to save

def save_high_score(name, score):
  # Open the CSV file in append mode
  with open('high_scores.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Read existing scores (if any)
    scores = []
    with open('high_scores.csv', 'r', newline='') as f:
      reader = csv.reader(f)
      for row in reader:
        scores.append((row[0], int(row[1])))  # Assuming name and score columns

    # Add the new score
    scores.append((name, score))

    # Sort scores by score (descending)
    scores.sort(key=lambda x: x[1], reverse=True)

    # Cap the number of scores
    scores = scores[:MAX_SCORES]

    # Write the capped list of scores back to the CSV
    writer.writerows(scores)

def load_high_scores():
  scores = []
  with open('high_scores.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      scores.append((row[0], int(row[1])))  # Assuming name and score columns
  return scores

# Example usage
save_high_score("Alice", 1000)
save_high_score("Bob", 800)
save_high_score("Charlie", 900)  # This will push out the lowest score
high_scores = load_high_scores()
print(high_scores)
