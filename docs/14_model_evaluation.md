# Model Evaluation

## 1. Objective

The objective is to evaluate the movie recommendation system using rating prediction accuracy, recommendation quality, and model training time.

## 2. Dataset Split

The MovieLens 1M dataset is divided into:
- 80% training data
- 20% testing data

The split uses random seed 42.

## 3. Evaluation Metrics

### RMSE
Measures the square root of the average squared prediction error. Lower values indicate better accuracy.

### MAE
Measures the average absolute difference between actual and predicted ratings. Lower values indicate better accuracy.

### Precision@10
Measures the proportion of the top 10 recommended movies that are relevant.

### Recall@10
Measures the proportion of relevant test movies recovered in the top 10 recommendations.

### Training Time
Measures the elapsed time required to train the ALS model.

## 4. Experimental Results

Insert the actual measured RMSE, MAE, Precision@10, Recall@10, and training time from the Colab experiment.

## 5. Discussion

Discuss the observed prediction accuracy, recommendation quality, computational cost, and limitations of the experiment.

## 6. Conclusion

The evaluation provides quantitative evidence of the ALS model's performance on the MovieLens 1M dataset.
