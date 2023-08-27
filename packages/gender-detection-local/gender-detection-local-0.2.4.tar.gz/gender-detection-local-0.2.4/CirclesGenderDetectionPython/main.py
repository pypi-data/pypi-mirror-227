from gender_detection import *

model=GenderClassifier()
result=model.predict_gender(model_path="gender_detection")
print(result)
