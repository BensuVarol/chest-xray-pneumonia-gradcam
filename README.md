\# Chest X-Ray Pneumonia Classification with Grad-CAM



MobileNetV2 transfer learning model for Normal vs Pneumonia chest X-ray classification with Grad-CAM visualization.



\## Overview



This project uses a deep learning model to classify chest X-ray images as either Normal or Pneumonia.



The model is based on MobileNetV2 and uses transfer learning. Grad-CAM is also included to visualize which regions of the chest X-ray influenced the model's prediction.



\## Dataset



The project uses the Chest X-Ray Images (Pneumonia) dataset from Kaggle.



The dataset is downloaded inside the notebook using the Kaggle API. When running the notebook in Google Colab, a Kaggle username and API token are required.



The dataset is not included in this repository.



\## Model



\- MobileNetV2 transfer learning

\- Binary classification: Normal vs Pneumonia

\- Fine-tuning

\- Class weights for class imbalance

\- Grad-CAM explainability



\## Evaluation



The model was evaluated using:



\- Accuracy

\- Precision

\- Recall

\- AUC

\- Classification report

\- Confusion matrix



A decision threshold of 0.85 was selected to reduce false positives while keeping pneumonia recall high.



\## Results



At threshold 0.85, the model achieved:



\- Accuracy: 91.51%

\- Precision: 90.80%

\- Recall: 96.15%

\- False Positives: 38

\- False Negatives: 15



\## Grad-CAM



Grad-CAM visualizations are used to inspect which parts of the X-ray image contributed most to the model's prediction.



This helps make the model more interpretable instead of only showing the final classification result.



\## How to Run



1\. Open the notebook in Google Colab.

2\. Enable GPU runtime.

3\. Enter your Kaggle username and API token when prompted.

4\. Run the notebook cells in order.



\## Note



This project is for educational and research purposes only. It is not intended for clinical diagnosis.

