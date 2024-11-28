import string
import re
import traceback
import pke
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor

# Ensure the necessary NLTK data files are downloaded
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('punkt_tab')


def generate_fill_in_the_blanks(text):
    def tokenize_sentences(text):
        sentences = sent_tokenize(text)
        return [sentence.strip() for sentence in sentences if len(sentence) > 20]

    def get_noun_adj_verb(text):
        out = []
        try:
            extractor = pke.unsupervised.MultipartiteRank()
            extractor.load_document(input=text, language='en')
            pos = {'NOUN', 'ADJ', 'VERB'}
            stoplist = list(string.punctuation)
            stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
            stoplist += stopwords.words('english')
            extractor.candidate_selection(pos=pos)
            extractor.candidate_weighting(alpha=1.1, threshold=0.75, method='average')
            keyphrases = extractor.get_n_best(n=30)

            for val in keyphrases:
                out.append(val[0])
        except Exception as e:
            print("Error in get_noun_adj_verb:", e)
            traceback.print_exc()
            out = []

        return out

    def get_sentences_for_keyword(keywords, sentences):
        keyword_processor = KeywordProcessor()
        keyword_sentences = {}
        for word in keywords:
            keyword_sentences[word] = []
            keyword_processor.add_keyword(word)
        for sentence in sentences:
            keywords_found = keyword_processor.extract_keywords(sentence)
            for key in keywords_found:
                keyword_sentences[key].append(sentence)

        for key in keyword_sentences.keys():
            values = keyword_sentences[key]
            values = sorted(values, key=len, reverse=True)
            keyword_sentences[key] = values
        return keyword_sentences

    def get_fill_in_the_blanks(sentence_mapping):
        out = {"title": "Fill in the blanks for these sentences with matching words at the top"}
        blank_sentences = []
        processed = []
        keys = []
        for key in sentence_mapping:
            if len(sentence_mapping[key]) > 0:
                sent = sentence_mapping[key][0]
                insensitive_sent = re.compile(re.escape(key), re.IGNORECASE)
                no_of_replacements = len(re.findall(re.escape(key), sent, re.IGNORECASE))
                line = insensitive_sent.sub(' _________ ', sent)
                if (sentence_mapping[key][0] not in processed) and no_of_replacements < 2:
                    blank_sentences.append(line)
                    processed.append(sentence_mapping[key][0])
                    keys.append(key)
        out["sentences"] = blank_sentences[:10]
        out["keys"] = keys[:10]
        return out

    # Main logic
    sentences = tokenize_sentences(text)
    noun_verbs_adj = get_noun_adj_verb(text)
    keyword_sentence_mapping_noun_verbs_adj = get_sentences_for_keyword(noun_verbs_adj, sentences)
    fill_in_the_blanks = get_fill_in_the_blanks(keyword_sentence_mapping_noun_verbs_adj)

    return fill_in_the_blanks

# Example usage:
# text_input = "President Donald Trump said and predicted that some states would reopen this month."
# text_input = """The theory of special relativity finds a convenient formulation in Minkowski spacetime, a mathematical structure that combines three dimensions of space with a single dimension of time. In this formalism, distances in space can be measured by how long light takes to travel that distance, e.g., a light-year is a measure of distance, and a meter is now defined in terms of how far light travels in a certain amount of time. Two events in Minkowski spacetime are separated by an invariant interval, which can be either space-like, light-like, or time-like. Events that have a time-like separation cannot be simultaneous in any frame of reference, there must be a temporal component (and possibly a spatial one) to their separation. Events that have a space-like separation will be simultaneous in some frame of reference, and there is no frame of reference in which they do not have a spatial separation. Different observers may calculate different distances and different time intervals between two events, but the invariant interval between the events is independent of the observer (and his velocity)."""
# fill_in_the_blanks = generate_fill_in_the_blanks(text_input)
# # Extract keywords from the fill-in-the-blank result
# extracted_keywords = fill_in_the_blanks['keys']
# generated_sentences = fill_in_the_blanks['sentences']

# # Print the extracted keywords and fill-in-the-blank sentences
# print("Extracted Keywords:")
# print(extracted_keywords)
# print("\nFill in the Blank Sentences:")
# for sentence in generated_sentences:
#     print(sentence)