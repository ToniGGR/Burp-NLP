import pandas as pd

abbreviations_dict = {
    "don’t": "do not",
    "isn’t": "is not",
    "ain’t": "is not",
    "gotta": "got to",
    "can’t": "cannot",
    "won’t": "will not",
    "you’re": "you are",
    "they’re": "they are",
    "we’re": "we are",
    "I’m": "I am",
    "she’s": "she is",
    "he’s": "he is",
    "it’s": "it is",
    "there’s": "there is",
    "what’s": "what is",
    "here’s": "here is",
    "that’s": "that is",
    "who’s": "who is",
    "how’s": "how is",
    "aren’t": "are not",
    "wasn’t": "was not",
    "weren’t": "were not",
    "doesn’t": "does not",
    "didn’t": "did not",
    "hasn’t": "has not",
    "haven’t": "have not",
    "hadn’t": "had not",
    "shouldn’t": "should not",
    "wouldn’t": "would not",
    "couldn’t": "could not",
    "mustn’t": "must not",
    "mightn’t": "might not",
    "needn’t": "need not",
    "let’s": "let us",
    "y’all": "you all",
    "gonna": "going to",
    "wanna": "want to",
    "lemme": "let me",
    "gimme": "give me",
    "kinda": "kind of",
    "sorta": "sort of",
    "outta": "out of",
    "lotta": "lot of",
    "dunno": "do not know",
    "c’mon": "come on",
    "o’clock": "of the clock",
    "y’know": "you know",
    "ma’am": "madam",
    "could’ve": "could have",
    "should’ve": "should have",
    "would’ve": "would have",
    "might’ve": "might have",
    "must’ve": "must have",
    "there’d": "there would",
    "it’d": "it would",
    "he’d": "he would",
    "she’d": "she would",
    "they’d": "they would",
    "I’d": "I would",
    "you’d": "you would",
    "we’d": "we would", 
    "it’s" : "it is"
}

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """führt verschiedene Data Cleaning Schritte über den Dataframe des Rick und Morty Datensatzes durch und gibt den gesäuberten Dataframe zurück"""
    # entferne \n (Absätze) und Leerzeichen
    df["dialouge"] = pd.Series( x.replace("\n", " ").replace("  ", "") for x in df["dialouge"])

    # entferne :
    df["speaker"] = df["speaker"].str.strip(":")

    #lowercase
    df['dialouge'] = df["dialouge"].apply(lambda x: x.lower())

    # ' -> ’
    df["dialouge"] = pd.Series( x.replace("'", "’")for x in df["dialouge"])

    # Abreviations
    corrected_row = []
    for row in df["dialouge"]:
        for entry in list(abbreviations_dict.keys()):
            if entry in row:
                row = row.replace(entry, abbreviations_dict[entry])
            continue 
        corrected_row.append(row)

    df["dialouge"] = pd.Series(corrected_row)

    # entferne nicht alphanumerische Zeichen
    df["dialouge"] = df["dialouge"].str.replace("[^\w\s]","" , regex=True)

    return df

