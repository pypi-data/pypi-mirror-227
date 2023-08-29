import asyncio
from pathlib import Path
import pickle
from typing import Optional

from typer import Typer

app = Typer()


@app.command()
def fetch_documents(config_path: Optional[str] = None, data_path: Optional[str] = None):
    """Fetches data from the API."""
    from docsrag.docs_fetcher import DocumentFetcher
    from docsrag.utils import load_config, get_data_path

    config = load_config(config_path)
    doc_fetcher = DocumentFetcher.parse_obj(config["fetch_docs"])

    data_path_to_use = Path(data_path) if data_path is not None else get_data_path()
    docs_dir = data_path_to_use / "docs"
    docs_dir.mkdir(exist_ok=True, parents=True)
    docs_path = docs_dir / f"{hash(doc_fetcher)}.pkl"

    if docs_path.exists():
        with open(docs_path, "rb") as f:
            documents = pickle.load(f)

    else:
        documents = asyncio.run(doc_fetcher.run())
        with open(docs_path, "wb") as f:
            pickle.dump(documents, f)


@app.command()
def parse_nodes(config_path: Optional[str] = None, data_path: Optional[str] = None):
    """Parses nodes from documents."""
    from docsrag.docs_fetcher import DocumentFetcher
    from docsrag.node_parser import NodeParser
    from docsrag.utils import load_config, get_data_path

    config = load_config(config_path)

    loader = DocumentFetcher.parse_obj(config["fetch_docs"])

    data_path_to_use = Path(data_path) if data_path is not None else get_data_path()
    docs_dir = data_path_to_use / "docs"
    docs_dir.mkdir(exist_ok=True, parents=True)
    docs_path = docs_dir / f"{hash(loader)}.pkl"

    if not docs_path.exists():
        raise ValueError(
            f"Docs not found at {docs_path}. "
            "Run `docsrag fetch-documents` to generate them."
        )

    parser = NodeParser.parse_obj(config["generate_nodes"])
    nodes_dir = data_path_to_use / "nodes"
    nodes_dir.mkdir(exist_ok=True, parents=True)
    nodes_path = nodes_dir / f"{hash(parser)}.pkl"

    if not nodes_path.exists():
        with open(docs_path, "rb") as f:
            documents = pickle.load(f)
        nodes = parser.run(documents)
        with open(nodes_path, "wb") as f:
            pickle.dump(nodes, f)


@app.command()
def build_vector_store(
    config_path: Optional[str] = None, data_path: Optional[str] = None
):
    """Builds the vector store."""
    from docsrag.node_parser import NodeParser
    from docsrag.utils import load_config, get_data_path
    from docsrag.vector_store_builder import VectorStore

    config = load_config(config_path)
    parser = NodeParser.parse_obj(config["generate_nodes"])

    data_path_to_use = Path(data_path) if data_path is not None else get_data_path()
    nodes_dir = data_path_to_use / "nodes"
    nodes_dir.mkdir(exist_ok=True, parents=True)
    nodes_path = nodes_dir / f"{hash(parser)}.pkl"

    if not nodes_path.exists():
        raise ValueError(
            f"Nodes not found at {nodes_path}. Run `docsrag parse-nodes` to generate them."
        )

    with open(nodes_path, "rb") as f:
        nodes = pickle.load(f)

    vector_store = VectorStore.parse_obj(config["build_vector_store"])
    vector_store_dir = data_path_to_use / "vector_store"
    vector_store_path = vector_store_dir / f"{hash(vector_store)}"
    if vector_store_path.exists():
        return

    vector_store_path.mkdir(exist_ok=True, parents=True)
    vector_store.update(nodes=nodes, persist_dir=vector_store_path)


@app.command()
def generate_evaluation_dataset(
    config_path: Optional[str] = None, data_path: Optional[str] = None
):
    """Generates the evaluation dataset."""
    from docsrag.utils import get_data_path, load_config
    from docsrag.evaluation_dataset_generator import EvaluationDatasetBuilder
    from docsrag.node_parser import NodeParser

    config = load_config(config_path)

    parser = NodeParser.parse_obj(config["generate_nodes"])
    data_path_to_use = Path(data_path) if data_path is not None else get_data_path()
    nodes_dir = data_path_to_use / "nodes"
    nodes_dir.mkdir(exist_ok=True, parents=True)
    nodes_path = nodes_dir / f"{hash(parser)}.pkl"

    if not nodes_path.exists():
        raise ValueError(
            f"Nodes not found at {nodes_path}. "
            "Run `docsrag parse-nodes` to generate them."
        )

    with open(nodes_path, "rb") as f:
        nodes = pickle.load(f)

    eval_data_builder = EvaluationDatasetBuilder.parse_obj(
        config["generate_evaluation_dataset"]
    )
    eval_data_dir = data_path_to_use / "eval_data"
    eval_data_path = eval_data_dir / f"{hash(eval_data_builder)}"
    if eval_data_path.exists():
        return

    eval_data_path.mkdir(exist_ok=True, parents=True)
    df = eval_data_builder.build(nodes)
    df.to_parquet(eval_data_path / "data.parquet")


@app.command()
def evaluate_vector_store(
    config_path: Optional[str] = None, data_path: Optional[str] = None
):
    """Evaluates the vector store."""
    from docsrag.utils import get_data_path, load_config
    from docsrag.vector_store_evaluator import VectorStoreEvaluator

    config = load_config(config_path)
    evaluator = VectorStoreEvaluator.parse_obj(config["evaluate_vector_store"])
    evaluator.evaluation_dataset_dir = (
        Path(data_path) if data_path is not None else get_data_path()
    )
    evaluator.run()


if __name__ == "__main__":
    app()
