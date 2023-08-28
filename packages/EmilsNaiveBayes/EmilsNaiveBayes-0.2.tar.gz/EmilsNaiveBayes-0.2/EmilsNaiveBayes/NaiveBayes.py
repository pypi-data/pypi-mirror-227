import json
import time
import logging
import math


class NaiveBayes:
    def __init__(
            self,
            binary_mode=True,
            consider_negation=True,
            filename="f_twitter_training.json",
            negation_words_file="negations.json",
            negation_punctuation_file="punctuation.json",
            training_datasets_path="training_datasets/",
            trained_datasets_path="trained_datasets/",
            remove_chars=None,
            line_limit=-1,  # -1 for unlimited
            enable_log_space=True,
            multiply_label_probability=True,
            chance_output_digits=3,
            logging_level=logging.DEBUG
    ):
        self.binary_mode = binary_mode
        self.filename = filename
        self.consider_negation = consider_negation
        self.negation_words_file = negation_words_file
        self.negation_punctuation_file = negation_punctuation_file
        self.training_datasets_path = training_datasets_path
        self.trained_datasets_path = trained_datasets_path
        self.remove_chars = remove_chars if remove_chars is not None else \
            [",", ";", ".", ":", "-", "'", "+", "*", "~", "`", "?", "\\", "!", '"', "&", "/"]
        self.line_limit = line_limit
        self.enable_log_space = enable_log_space
        self.multiply_label_probability = multiply_label_probability
        self.chance_output_digits = chance_output_digits

        logging.basicConfig(level=logging_level, format="(%(asctime)s) [%(name)s] [%(levelname)s] %(message)s")

        self.labels = []
        self.label_word_bags = {}
        self.total_words = 0
        self.label_probabilities = {}
        self.label_total_words = {}

    @property
    def training_file(self):
        return self.training_datasets_path + self.filename

    @property
    def output_file(self):
        return self.trained_datasets_path + "trained_" + ('binary_' if self.binary_mode else '') + self.filename

    @property
    def negation_words(self):
        return json.load(open(self.negation_words_file))

    @property
    def punctuation(self):
        return json.load(open(self.negation_punctuation_file))

    def load(self, trained_filename: str):
        with open(self.trained_datasets_path + trained_filename, "r") as f:
            trained_data = json.load(f)
            self.label_word_bags = trained_data["LABEL_WORD_BAGS"]
            self.labels = trained_data["LABELS"]
            self.label_total_words = trained_data["LABEL_TOTAL_WORDS"]
            self.label_probabilities = trained_data["LABEL_PROBABILITIES"]
            self.total_words = trained_data["TOTAL_WORDS"]

    def sample_word(self, word: str):
        word_sample = word.lower()
        for char in self.remove_chars:
            word_sample = word_sample.replace(char, "")
            return word_sample

    def sample_text(self, text: str):
        text_sample = text.lower()
        if self.consider_negation:
            i = 0
            negated = False
            while i < len(text_sample):
                if not negated:
                    for negation_word in self.negation_words:
                        if text_sample[i:i + len(negation_word)] == negation_word:
                            negated = True
                elif text_sample[i] in self.punctuation:
                    negated = False
                if negated and text_sample[i] == " ":
                    text_sample = text_sample[:i + 1] + "NOT_" + text_sample[i + 1:]
                    i += 5
                else:
                    i += 1
        for char in self.remove_chars:
            text_sample = text_sample.replace(char, "")
        pass
        text_sample = [e for e in text_sample.split(" ") if e not in ["NOT_", ""]]
        text_sample = list(set(text_sample)) if self.binary_mode else text_sample
        return text_sample
    
    def get_word_bag(self, text: str):
        bag = {}
        text_sample = self.sample_text(text)
        for word in text_sample:
            if word in bag.keys():
                bag[word] += 1
            else:
                bag[word] = 1
        return bag

    def save_as_file(self):
        logging.debug("Creating output file")
        open(self.output_file, "w").close()

        logging.debug("Writing to output file")
        with open(self.output_file, "w") as f:
            f.write(json.dumps({
                "TOTAL_WORDS": self.total_words,
                "LABELS": self.labels,
                "LABEL_PROBABILITIES": self.label_probabilities,
                "LABEL_TOTAL_WORDS": self.label_total_words,
                "LABEL_WORD_BAGS": self.label_word_bags
            }))

    def get_word_label_probability(self, word: str, label: str):
        word_sample = self.sample_word(word)
        if word_sample in self.label_word_bags[label].keys():
            word_occurrences = self.label_word_bags[label][word_sample] + 1
            total_words_in_label_bag = self.label_total_words[label]
            return word_occurrences / total_words_in_label_bag
        else:
            return 1 / (self.total_words + 1)

    def get_label_text_probability(self, label: str, text: str):
        label_probability = self.label_probabilities[label]
        text_sample = self.sample_text(text)
        if self.enable_log_space:
            text_probability = 0
            for word in text_sample:
                text_probability += math.log(self.get_word_label_probability(word, label))
            return math.exp(text_probability + (math.log(label_probability) if self.multiply_label_probability else 0))
        else:
            text_probability = 1
            for word in text_sample:
                text_probability *= self.get_word_label_probability(word, label)
            return text_probability * (label_probability if self.multiply_label_probability else 1)

    def evaluate(self, input_text):
        probabilities = {}
        for label in self.labels:
            probabilities[label] = self.get_label_text_probability(label, input_text)
        total_probability = sum(probabilities.values())
        percentages = {}
        for label, probability in probabilities.items():
            coefficent = 10 ** self.chance_output_digits
            percentages[label] = str(int(probability / total_probability * 100 * coefficent) / coefficent) + "%"

        return {
            "rating": max(probabilities, key=probabilities.get),
            "percentages": percentages
        }

    def test(self, input_text=None):
        if input_text is None:
            input_text = input("Input text: ")
        res = self.evaluate(input_text)
        print("Bewertung: %s " % res["rating"])
        print("Chancen: %s" % res["percentages"])

    def train(self):
        logging.info("Beginning with Training")
        start_time = time.time()

        logging.debug("Initializing variables")
        self.label_word_bags = {}
        label_occurrences = {}
        total_length = 0
        self.total_words = 0
        logging.debug("Building label word bags, label occurrences")
        with open(self.training_file, "r") as f:
            line = f.readline()
            while len(line) != 0 and total_length != self.line_limit:

                total_length += 1
                print(f"\rProcessing line: {total_length}", end="")

                line_loaded = json.loads(line)
                text = line_loaded["text"]
                label = line_loaded["label"]

                if label not in self.labels:
                    label_occurrences[label] = 1
                    self.labels.append(label)
                    self.label_word_bags[label] = {}
                else:
                    label_occurrences[label] += 1

                word_bag = self.get_word_bag(text)
                self.total_words += len(word_bag)

                for word, times in word_bag.items():
                    try:
                        self.label_word_bags[label][word] += times
                    except KeyError:
                        self.label_word_bags[label][word] = times

                line = f.readline()
        print("\r", end="")
        logging.info(f"Total lines processed: {total_length}")
        logging.info(f"Total words processed: {self.total_words}")

        logging.debug(f"Built label word bags, label occurences")

        logging.debug("Calculating label specific properties")
        self.label_probabilities = {}
        self.label_total_words = {}
        for label in self.labels:
            self.label_probabilities[label] = label_occurrences[label] / total_length
            self.label_total_words[label] = sum(self.label_word_bags[label].values())

        end_time = time.time()
        training_seconds = end_time - start_time
        logging.info(f"Training finished successfully, took {training_seconds} seconds")
