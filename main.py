import pandas as pd


from content_scrapper import ContentScrapper

if __name__ == "__main__":
    URL = "https://eur-lex.europa.eu/legal-content/PL/TXT/HTML/?uri=OJ:L_202400601&qid=1720526534324"

    cs = ContentScrapper(URL)
    document_metadata = cs.get_document_metadata()
    metadata_df = pd.DataFrame([document_metadata])
    print(metadata_df)
