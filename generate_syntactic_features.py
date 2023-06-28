import pandas as pd
import spacy
from collections import defaultdict
from argparse import ArgumentParser
import tqdm

POSTAGS = {"pronouns": "PRON", "auxiliaries": "AUX", "subordinating_conjunctions": "SCONJ",
           "adverbs": "ADV", "nouns": "NOUN", "prepositions": "ADP", "numbers": "NUM", "verbs": "VERB"}


def get_amount_pos_tags(comment, pos_tags):
    # generate a dictionary that contains the amount of each pos tag
    pos_tag_dict = defaultdict(int)
    # for each tag in pos_tags, set the initial value to 0
    for tag in pos_tags:
        pos_tag_dict[tag] = 0
    for token in comment:
        pos_tag = token.pos_
        if pos_tag in pos_tags:
            pos_tag_dict[pos_tag] += 1
    # convert the counts to percentages
    for pos_tag in pos_tag_dict:
        pos_tag_dict[pos_tag] = pos_tag_dict[pos_tag] / len(comment)
    return pos_tag_dict


def get_morophology(comment):
    frequency_past_adverbs = 0
    frequency_imperative = 0
    frequency_first_person = 0
    for token in comment:
        morph = token.morph
        if "Tense=Past" in morph:
            frequency_past_adverbs += 1
        if "Mood=Imp" in morph:
            frequency_imperative += 1
        if "Person=1" in morph:
            frequency_first_person += 1
    return {"past_tense": frequency_past_adverbs / len(comment), "imperative": frequency_imperative / len(comment),
            "first_person": frequency_first_person / len(comment)}


def get_amount_entities(comment):
    frequency_entities = 0
    for token in comment:
        if token.ent_iob_ == "B":
            frequency_entities += 1
    return frequency_entities / len(comment)


def pipeline(input_path, model_identifier, output_path, comment_column):
    # check if model_identifier exists, or download it
    try:
        model = spacy.load(model_identifier, disable=["parser"])
    except OSError:
        print("Model not found, downloading it now.")
        spacy.cli.download(model_identifier)
        model = spacy.load(model_identifier, disable=["parser"])

    # load data
    data = pd.read_csv(input_path, sep="\t")
    comments = list(data[comment_column])
    print("number of comments: ", len(comments))
    # create a dictionary of lists that contains all features as keys
    features = defaultdict(list)
    for doc in tqdm.tqdm(model.pipe(comments)):
        pos_tag_dic = get_amount_pos_tags(doc, list(POSTAGS.values()))
        amount_entities = get_amount_entities(doc)
        amount_morph_dic = get_morophology(doc)
        for k, v in amount_morph_dic.items():
            features[k].append(v)
        length = len(doc)
        for k, v in pos_tag_dic.items():
            features[k].append(v)
        features["entities"].append(amount_entities)
        features["num_tokens"].append(length)
    print("number of instances with features: ", len(features["num_tokens"]))
    # add each feature as column to the dataframe
    for k, v in features.items():
        data[k] = v
    # save new dataframe to output path
    data.to_csv(output_path, sep="\t", index=False)
    print("saved dataframe to %s" % output_path)


if __name__ == '__main__':
    # parse arguments, input_path, output_path
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_path", dest="input_path", help="path to input file")
    parser.add_argument("-o", "--output_path", dest="output_path", help="path to output file")
    # which column stores the comments?
    parser.add_argument("-c", "--comment_column", dest="comment_column", help="name of column that stores comments")
    # add spacy model as optional argument with default value
    parser.add_argument("-m", "--model", dest="model", help="spacy model to use", default="en_core_web_sm")
    args = parser.parse_args()
    pipeline(args.input_path, args.model, args.output_path, args.comment_column)


