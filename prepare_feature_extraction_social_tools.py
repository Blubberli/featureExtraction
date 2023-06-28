import pandas as pd
from argparse import ArgumentParser
import tqdm

if __name__ == '__main__':
    # parse arguments, input_path, output_path
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_path", dest="input_path", help="path to input file")
    # which column stores the comments?
    parser.add_argument("-c", "--comment_column", dest="comment_column", help="name of column that stores comments")
    # which column stores comment IDs? (optional)
    parser.add_argument("-id", "--id_column", dest="id_column", help="name of column that stores comment IDs", default=None)

    # read in the dataset
    args = parser.parse_args()
    data = pd.read_csv(args.input_path, sep="\t")
    # check if column with comment IDs is given otherwise create an id column and ids for the comments
    if not args.id_column:
        id_list = list(range(0, len(data)))
        # add "ID" before every number
        id_list = ["ID%d" % el for el in id_list]
        data["ID"] = id_list
        id_col = "ID"
    else:
        id_list = data[args.id_column].tolist()
        id_col = args.id_column
    print("generating text files...")
    # iterate over id and comment and create a textfile named as ID (.txt) containing the text as content
    for commentID in tqdm.tqdm(id_list):
        comment = data[data[id_col] == commentID][args.comment_column].tolist()[0]
        # create filename in ./textfiles with commentID + ".txt" and write comment to it
        with open("./textfiles/%s.txt" % commentID, "w") as file:
            file.write(comment)
    print("generated %d text files" % len(id_list))