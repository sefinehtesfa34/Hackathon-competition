from django.apps import AppConfig
# from sklearn.model_selection import train_test_split
import re
import string
import tensorflow as tf
# from tensorflow import keras
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import nltk
# from nltk.corpus import stopwords
import warnings
import pickle
# import os
# import shutil
import tensorflow as tf
# import tensorflow_hub as hub
# import tensorflow_text as text
# from official.nlp import optimization  # to create AdamW optimizer
# import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.preprocessing import LabelEncoder

tf.get_logger().setLevel('ERROR')

resume_df=pd.read_csv("connector/dataset/resume.csv")

warnings.filterwarnings('ignore')
# nltk.download('stopwords')

# Create a custom standardization function to strip HTML break tags '<br />'.
def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
    return tf.strings.regex_replace(stripped_html,
                                  '[%s]' % re.escape(string.punctuation), '')


# Vocabulary size and number of words in a sequence.
vocab_size = 10000
sequence_length = 300

# Use the text vectorization layer to normalize, split, and map strings to
# integers. Note that the layer uses the custom standardization defined above.
# Set maximum_sequence length as all samples are not of the same length.
vectorize_layer = tf.keras.layers.TextVectorization(
    standardize=custom_standardization,
    max_tokens=vocab_size,
    output_mode='int',
    output_sequence_length=sequence_length)

vectorize_layer.adapt(resume_df["Resume"].values)

with open('connector/machine_learning_models/dict.pickle', 'rb') as handle:
    dict_model = pickle.load(handle)


new_model=tf.keras.models.load_model("connector/machine_learning_models/model",\
                                     custom_objects={'vectorize_layer':vectorize_layer,\
                                                    "custom_standardization":custom_standardization})

class ConnectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'connector'
    dict_model=dict_model
    model=new_model


