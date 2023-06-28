import readability
import pandas as pd
import spacy
from collections import defaultdict
from argparse import ArgumentParser
import tqdm


def pipeline(input_path, model_identifier, output_path, comment_column):
    try:
        model = spacy.load(model_identifier, disable=["attribute_ruler", "lemmatizer"])
    except OSError:
        print("Model not found, downloading it now.")
        spacy.cli.download(model_identifier)
        model = spacy.load(model_identifier, disable=["attribute_ruler", "lemmatizer"])

    # load data
    data = pd.read_csv(input_path, sep="\t")
    comments = list(data[comment_column])
    # create a dictionary of lists that contains all features as keys
    features = defaultdict(list)
    print("extracting features...")
    for doc in tqdm.tqdm(model.pipe(comments)):
        tokenized = '\n'.join(' '.join(str(token) for token in sentence)
                              for sentence in doc.sents)
        results = readability.getmeasures(tokenized, lang='en')
        # readability
        flesch = results["readability grades"]["FleschReadingEase"]
        gunningFog = results["readability grades"]["GunningFogIndex"]
        # sentence info
        characters_per_word = results["sentence info"]["characters_per_word"]
        syll_per_word = results["sentence info"]["syll_per_word"]
        ttr = results["sentence info"]["type_token_ratio"]
        long_words = results["sentence info"]["long_words"] / len(doc)
        complex_words = results["sentence info"]["complex_words"] / len(doc)
        # add features to dictionary
        features["flesch"].append(flesch)
        features["gunningFog"].append(gunningFog)
        features["characters_per_word"].append(characters_per_word)
        features["syll_per_word"].append(syll_per_word)
        features["ttr"].append(ttr)
        features["long_words"].append(long_words)
        features["complex_words"].append(complex_words)
    for k, v in features.items():
        data[k] = v
    # write to csv
    data.to_csv(output_path, sep="\t", index=False)
    print("features written to %s" % output_path)


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
