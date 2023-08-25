from contextualized_topic_models.models.ctm import CombinedTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
from contextualized_topic_models.utils.preprocessing import WhiteSpacePreprocessingStopwords
from contextualized_topic_models.evaluation.measures import CoherenceNPMI

import nltk
from nltk.corpus import stopwords as stop_words
from few_shot_priming.prompting_stance import *
from few_shot_priming.experiment import *
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

split = load_splits("ibmsc")
documents = split["validation"]["text"]
stopwords = list(stop_words.words("english"))
sp = WhiteSpacePreprocessingStopwords(documents, stopwords_list=stopwords)
preprocessed_documents, unpreprocessed_corpus, vocab, retained_indices = sp.preprocess()
tp = TopicModelDataPreparation("all-mpnet-base-v2")
training_dataset = tp.fit(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)
documents = [document.split() for document in documents]
for n in range(10,40,5):
	ctm = CombinedTM(bow_size=len(tp.vocab), contextual_size=768, n_components=n, num_epochs=100)
	ctm.fit(training_dataset)
	npmi = CoherenceNPMI(texts=documents, topics=ctm.get_topic_lists(10))
	print(npmi.score(),n)
