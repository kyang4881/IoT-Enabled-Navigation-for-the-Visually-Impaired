import accelerate
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline as ppl
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import HuggingFacePipeline
from langchain.vectorstores import Chroma

class LLMInterface:
    """Interface for Language Models and Retrieval System."""
    def __init__(self, file_name, model_name, embedding_model_name):
        """
        Initialize LLMInterface.

        Args:
        - file_name (str): Name of the file to load.
        - model_name (str): Name of the language model to use.
        - embedding_model_name (str): Name of the embedding model to use.
        """
        self.retriever=None
        self.llm=None
        self.model=self.load_quantized_model(model_name)
        self.tokenizer=self.initialize_tokenizer(model_name)
        self.file_name = file_name
        self.embedding_model_name = embedding_model_name
        self.chat_histories = []

        self.debugLoader()
        
    def debugLoader(self):
        """Load documents and set up retriever and language model pipeline."""
        loader = PyPDFLoader(self.file_name)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
        all_splits = text_splitter.split_documents(documents)
        model_kwargs = {"device": "cpu"}
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name, model_kwargs=model_kwargs)
        vectordb = Chroma.from_documents(documents=all_splits, embedding=embeddings, persist_directory="chroma_db")
        self.retriever = vectordb.as_retriever()

        pipeline = ppl(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            use_cache=True,
            device_map="auto",
            max_length=2048,
            truncation=True,
            do_sample=True,
            top_k=5,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        self.llm = HuggingFacePipeline(pipeline=pipeline)


    def load_quantized_model(self,model_name: str):
        """
        Load a quantized language model.

        Args:
        - model_name (str): Name of the language model to load.

        Returns:
        - model: Loaded quantized language model.
        """
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        return model
    

    def initialize_tokenizer(self,model_name: str):
        """
        Initialize tokenizer for a given language model.

        Args:
        - model_name (str): Name of the language model.

        Returns:
        - tokenizer: Initialized tokenizer.
        """
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.bos_token_id = 1  
        return tokenizer
    

    def create_conversation(self,query: str, chat_history: list) -> tuple:
        """
        Create a conversation based on the query and chat history.

        Args:
        - query (str): Query for the conversation.
        - chat_history (list): History of the conversation.

        Returns:
        - tuple: Tuple containing an empty string and updated chat history.
        """
        try:
            memory = ConversationBufferMemory(
                memory_key='chat_history',
                return_messages=False
            )
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.retriever,
                memory=memory,
                get_chat_history=lambda h: h,
            )

            result = qa_chain({'question': query, 'chat_history': chat_history})
            chat_history.append((query, result['answer']))
            self.chat_histories.append(result['answer'])
            return '', chat_history


        except Exception as e:
            chat_history.append((query, e))
            return '', chat_history