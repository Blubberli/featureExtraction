import pandas as pd
from tabulate import tabulate
from argparse import ArgumentParser


def merge_features(input_path, idcol, polarity, syntax, surface, taales, taaled,
                   output_path, filter=False):
    # read in all data
    orig = pd.read_csv(input_path, sep="\t")
    pol = pd.read_csv(polarity)
    # add column commentID to pol (it is column filename with .txt removed)
    pol[idcol] = pol["filename"].apply(lambda x: x[:-4])
    # merge orig and pol on idcol, only keep columns from pol that are not in orig
    merged = pd.merge(orig, pol, on=idcol, how="left", suffixes=("", "_pol"))
    taales = pd.read_csv(taales)
    taales[idcol] = taales["Filename"].apply(lambda x: x[:-4])
    merged = pd.merge(merged, taales, on=idcol, how="left", suffixes=("", "_taales"))
    taaled = pd.read_csv(taaled)
    taaled[idcol] = taaled["filename"].apply(lambda x: x[:-4])
    merged = pd.merge(merged, taaled, on=idcol, how="left", suffixes=("", "_taaled"))
    surface = pd.read_csv(surface, sep="\t")
    # get column names that are not in merged already
    surface_cols = [col for col in surface.columns if col not in merged.columns]
    surface_cols.append(idcol)
    merged = pd.merge(merged, surface[surface_cols], on=idcol, how="left", suffixes=("", "_surface"))
    # merge on idcol but only add columns from surface that are not in merged
    syntax = pd.read_csv(syntax, sep="\t")
    syntax_cols = [col for col in syntax.columns if col not in merged.columns]
    syntax_cols.append(idcol)
    merged = pd.merge(merged, syntax[syntax_cols], on=idcol, how="left", suffixes=("", "_syntax"))
    print(tabulate(merged.head(), headers="keys", tablefmt="psql"))
    if filter:
        merged = filter_dataframe(merged)
    print("merged %d comments, %d features" % (len(merged), len(merged.columns)))
    #print(tabulate(merged.head(n=2), headers="keys", tablefmt="psql"))
    print(merged.head(n=2))
    print("writing merged data to %s" % output_path)
    merged.to_csv(output_path, sep="\t", index=False)


def filter_dataframe(df):
    """specify the corresponding columns for each feature set and filter out all columns that are not needed"""
    subset_diversity = open("subset_diversity.txt").read().splitlines()
    subset_polarity = open("subset_polarity.txt").read().splitlines()
    subset_taales = open("subset_sophistication.txt").read().splitlines()
    # join the lists
    subset = subset_diversity + subset_polarity + subset_taales
    # only keep columns that are in subset
    df = df[subset]
    return df


if __name__ == '__main__':
    # parse different filenames
    parser = ArgumentParser()
    parser.add_argument("-o", "--output_path", dest="output_path", help="path to output file")
    parser.add_argument("-i", "--input_path", dest="input_path", help="path to input file")
    parser.add_argument("-id", "--idcol", dest="idcol", help="name of id column")
    parser.add_argument("-su", "--surface", dest="surface", help="path to surface features")
    parser.add_argument("-sy", "--syntax", dest="syntax", help="path to syntax features")
    parser.add_argument("-p", "--polarity", dest="polarity", help="path to polarity features")
    parser.add_argument("-t", "--taales", dest="taales", help="path to taales features")
    parser.add_argument("-td", "--taaled", dest="taaled", help="path to taaled features")
    parser.add_argument("-f", "--filter", dest="filter", action="store_true",
                        help="filter out columns that are not needed")
    args = parser.parse_args()
    merge_features(args.input_path, args.idcol, args.polarity, args.syntax, args.surface, args.taales, args.taaled,
                     args.output_path, args.filter)

