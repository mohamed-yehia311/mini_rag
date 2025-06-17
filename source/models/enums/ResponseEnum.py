from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_FAILED = "Processing_Failed"
    FILE_PROCESSING_FAILD = "file_processing_failed"
    FILE_PROCESSING_SUCESS = "file_processing_success"
    NO_FILES_ERROR = "not_found_files"
    FILE_ID_ERROR = "no_file_found_with_this_id"
    PROCESSING_SUCCESS = "processing_success"
    PROJECT_NOT_FOUND_ERROR = "project_not_found"
    INSERT_INTO_VECTORDB_ERROR = "insert_into_vectordb_error"
    INSERT_INTO_VECTORDB_SUCCESS = "insert_into_vectordb_success"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb_collection_retrieved"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_success"
    RAG_ANSWER_SUCCESS = "rag_answer_success"