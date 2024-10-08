from medirag.core.data_manager import DailyMedDataManager
from medirag.core.document_processor import DailyMedDocumentProcessor
from medirag.index.local import DailyMedIndexer


def test_document_processor(data_dir):
    # Example usage:
    zip_file_path = data_dir.joinpath("dm_spl_release_human_rx_part0.zip")
    # Ensure the path is correct and the file exists
    assert zip_file_path.exists(), f"File not found: {zip_file_path}"

    download_sources = [zip_file_path.as_posix()]

    # Initialize and manage data
    data_manager = DailyMedDataManager(download_sources=download_sources)
    data_manager.download_and_extract_zip()
    extracted_dir = data_manager.get_extracted_dir()

    # Process documents
    document_processor = DailyMedDocumentProcessor(extracted_dir=extracted_dir)
    documents = document_processor.load_documents()

    assert len(documents) == 5

    # Index and query documents
    indexer = DailyMedIndexer()
    indexer.load_index(documents=documents)
    # indexer.save_index(persist_dir="../data/daily_bio_bert_indexed")

    query = "What are the key things about the drug's usage?"
    results = indexer.retrieve(query)

    assert len(results) > 0

    for result in results:
        print(result.text)
