import chromadb
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from app.config.settings import CHROMA_DB_PATH, COLLECTION_NAME


def visualize_embeddings_3d():
    """
    Visualize embeddings in 3D using PCA
    """
    print("Loading embeddings from ChromaDB...")

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    # Get more samples from different documents
    results = collection.get(
        limit=500,
        include=["embeddings", "documents", "metadatas"]
    )

    embeddings = np.array(results['embeddings'])
    sources = [
        m.get('source', 'unknown').split("\\")[-1].replace(".pdf", "").replace("SBP_", "")
        for m in results['metadatas']
    ]

    # Reduce to 3D using PCA
    print("Reducing to 3D with PCA...")
    pca = PCA(n_components=3)
    embeddings_3d = pca.fit_transform(embeddings)

    # Plot 3D
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Color by source
    unique_sources = list(set(sources))
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_sources)))

    for idx, source in enumerate(unique_sources):
        mask = [s == source for s in sources]
        x = embeddings_3d[mask, 0]
        y = embeddings_3d[mask, 1]
        z = embeddings_3d[mask, 2]
        ax.scatter(x, y, z, c=[colors[idx]], label=source[:20], alpha=0.7, s=20)

    ax.set_title("Embeddings Visualization (PCA 3D)")
    ax.set_xlabel("PCA 1")
    ax.set_ylabel("PCA 2")
    ax.set_zlabel("PCA 3")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=6)
    plt.tight_layout()

    # Save
    plt.savefig("./data/embeddings_3d_visualization.png", dpi=150)
    print(" Saved to data/embeddings_3d_visualization.png!")
    plt.show()


if __name__ == "__main__":
    visualize_embeddings_3d()