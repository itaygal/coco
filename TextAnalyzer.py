import gensim.models.keyedvectors as word2vec

class TextAnalyzer:
    __instance = None

    @staticmethod
    def get_instance():
        if TextAnalyzer.__instance is None:
            TextAnalyzer()
        return TextAnalyzer.__instance

    def __init__(self):
        if TextAnalyzer.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            super(TextAnalyzer, self).__init__()
            TextAnalyzer.__instance = self
            self.word2vec = word2vec.KeyedVectors.load_word2vec_format('.//GoogleNews-vectors-negative300.bin', binary=True)

    def parse(self, msg):
        msg = self.filter_letters(msg)
        msg_tokens = self.tokenize(msg)
        return msg_tokens

    def remove_stop_words(self, msgTokens):
        stopWords =  ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
                "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did",
                "do", "does", "doing", "during", "each", "few", "for", "from", "further", "had", "has", "have",
                "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
                "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its",
                "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or",
                "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll",
                "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
                "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
                "this", "those", "through", "to", "too", "under", "until", "very", "was", "we", "we'd", "we'll",
                "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while",
                "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've",
                "your", "yours", "yourself", "yourselves", "hi"]
        return [w for w in msgTokens if w not in stopWords]

    def filter_letters(self, msg):
        return ''.join([c for c in msg if c.isalpha() or c == ' '])

    def tokenize(self, msg):
        return msg.lower().split(' ')

    def for_coco(self, request_tokens):
        return "coco" in request_tokens

    def similarity_score(self, word_vector, word_vector2):
        similarity = 0.0
        word_count = 0
        vec1 = word_vector.copy()
        vec2 = word_vector2.copy()
        while len(vec1) != 0 and len(vec2) != 0:
            max_similarity = 0.0
            vec1_most_similar_word = ""
            vec2_most_similar_word = ""
            for word1 in vec1:
                for word2 in vec2:
                    word_similarity = self.word2vec.similarity(word1, word2)
                    if word_similarity > max_similarity:
                        max_similarity = word_similarity
                        vec1_most_similar_word = word1
                        vec2_most_similar_word = word2
            vec1.remove(vec1_most_similar_word)
            vec2.remove(vec2_most_similar_word)
            similarity += max_similarity
            word_count += 1
        return similarity/word_count
