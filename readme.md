## feature extraction for textual data

The following code can be used to extract features for text. The cover four broader categories:

- surface features
- syntactic features
- lexical diversity
- lexical sophistication
- polarity

### install the following packages:

- pandas
- spacy
- tqdm
- readability
- tabulate
  
To extract the features you need:

- a csv file with a column that contains your text data (e.g a column that contains forum posts or tweets)

The csv can have extra columns that will be retained after featurer extraction. It is beneficial if your csv file
already contains another column with unique identifier for your comments (e.g. "commentID") but if not the script
````prepare_feature_extraction_social_tools.py```` will add one for you.

Follow the follwing steps to extract features:

- (a)
  run the script ````prepare_feature_extraction_social_tools.py```` to prepare your data for feature extraction. This
  script will add a column with unique identifiers for your comments if you don't have one already. Make sure your
  column with the text doesn't contain any None or NaN values. The script will generate single textfiles in the
  directoy *textfiles* that contain the text of each comment. The textfiles will be named after the unique identifier of
  the comment.

- (b)
  download Seance from https://www.linguisticanalysistools.org/seance.html
  and install it. Run it and specify the directory with textfiles as input. Sepcify the name of the output file but
  don't store it in the same directory as the textfiles (e.g. store it in the dir *output*). The program will run in an
  interface and you will see when it stopped running. It will have created a new file with the extracted features. Mark
  all possible checkboxes.

- (c)
  download taaled from https://www.linguisticanalysistools.org/taaled.html
  and install it. Run it and specify the directory with textfiles as input. It looks like Seance. Select *all Words* and
  all availabe features. This will also create a csv file.

- (d)
  download taales from https://www.linguisticanalysistools.org/taales.html
  and install it. Note that if you have a newer mac this will not work on a mac but you have to use a linux or windows
  computer. Run it and specify the directory with textfiles as input. It looks like Seance and taaled. Select *spoken*
  checkbox if you are working with online forum posts or tweets (more formal texts you can select *news* or *academic*).
  This will also create a csv file.

- (e)
  run the script ````generate_surface_features.py```` and specificy your original csv file as input. It needs to have an
  ID column.

- (f)
  run the script ````generate_syntactic_features.py```` and specificy your original csv file as input. It needs to have
  an ID column. If there are more part-of-speech tags you can change the specified tag list in the script. (same for morphology).
  Also you may want to use a different spacy model. Check for the availble spacy models for english to find the most appropriate one.

- (g)
  Finally you have created all featuer sets. The last thing will be to merge them into one dataframe. For that you can
  run the script
  ````merge_features.py````. It will create a new csv file with all features. You need to specifiy all filepaths that
  you generated before. You can also filter the frame with pre-defined features. To pre-define them use the textfiles *
  subset_diversity.txt* and *subset_sophistication.txt* and  *subset_polarity*. 

Every tool that is used has a detailed spreadsheet that describes each featuer.
A summarized description of the main features I used can be found in the appendix in 
https://aclanthology.org/2022.acl-long.379.pdf

For a reference output check the csv files in the folder *output* and *textfiles*.
Clean the textfiles directory before and after every extraction or it will keep all of them.
