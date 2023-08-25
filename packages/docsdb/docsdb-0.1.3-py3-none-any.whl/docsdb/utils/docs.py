import os
import yaml


def create_docs_folder_structure(node, docs_path="docs"):
    if not os.path.exists(docs_path):
        os.mkdir(docs_path)

    for cluster, dbs in node.items():
        if cluster in {"meta", "started_at", "ended_at"}:
            continue
        cluster_path = os.path.join(docs_path, cluster)
        if not os.path.exists(cluster_path):
            os.mkdir(cluster_path)

        for dbName, db in dbs.items():
            db_path = os.path.join(cluster_path, dbName)
            if not os.path.exists(db_path):
                os.mkdir(db_path)

            db_yml_file = os.path.join(db_path, f"{dbName}.yml")
            if not os.path.exists(db_yml_file):
                open(db_yml_file, "w").close()

            collection_path = os.path.join(db_path, "collections")
            if not os.path.exists(collection_path):
                os.mkdir(collection_path)

            for collection in db.get("collections", []):
                file_name = f"{collection}.yml"
                collection_yml_file = os.path.join(collection_path, file_name)
                if not os.path.exists(collection_yml_file):
                    open(collection_yml_file, "w").close()


def docs_yaml_to_json(metadata, docs_path="docs"):
    docs_metadata = {}
    if os.path.exists(docs_path):
        for cluster, dbs in metadata.items():
            if cluster in {"meta", "started_at", "ended_at"}:
                continue
            cluster_path = os.path.join(docs_path, cluster)
            if not os.path.exists(cluster_path):
                continue
            docs_metadata[cluster] = {}
            for dbName, db in dbs.items():
                db_path = os.path.join(cluster_path, dbName)
                db_yml_file = os.path.join(db_path, f"{dbName}.yml")
                if not os.path.exists(db_yml_file):
                    continue
                with open(db_yml_file, "r") as file:
                    db_docs = yaml.safe_load(file)
                docs_metadata[cluster][dbName] = {}
                docs_metadata[cluster][dbName]["db"] = db_docs
                docs_metadata[cluster][dbName]["collections"] = {}

                collection_path = os.path.join(db_path, "collections")
                if not os.path.exists(collection_path):
                    continue

                for collection in db.get("collections", []):
                    file_name = f"{collection}.yml"
                    collection_yml_file = os.path.join(collection_path, file_name)
                    if not os.path.exists(collection_yml_file):
                        continue
                    with open(collection_yml_file, "r") as file:
                        collection_docs = yaml.safe_load(file)
                    docs_metadata[cluster][dbName]["collections"][
                        collection
                    ] = collection_docs
        return docs_metadata
    else:
        return docs_metadata
