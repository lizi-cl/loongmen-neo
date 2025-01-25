# Loongmen-Neo: Text-Based Copyright Infringement Detection Tool

## Overview

Loongmen-Neo is a powerful tool designed to detect potential copyright infringements in text-based content. By leveraging advanced embedding models and Weaviate's vector search capabilities, Loongmen-Neo scans and identifies similar content, generating detailed matching results. This tool is particularly useful for content creators, publishers, and legal professionals who need to ensure the originality of their work or identify unauthorized use of copyrighted material.

## Features

- **Embedding Models**: Utilizes state-of-the-art embedding models to convert text into high-dimensional vectors, capturing the semantic meaning of the content.
- **Weaviate Integration**: Integrates with Weaviate, a scalable and efficient vector search engine, to perform fast and accurate similarity searches.
- **Content Matching**: Scans large datasets to find text segments that are semantically similar to the input content, highlighting potential copyright infringements.
- **Detailed Reports**: Generates comprehensive reports with matching results, including similarity scores and relevant text excerpts.
- **Scalable**: Designed to handle large volumes of text data, making it suitable for both small-scale and enterprise-level applications.

## Snapshot
![snapshot](https://github.com/lizi-cl/loongmen-neo/blob/main/assets/result.png?raw=true)

## Installation

To get started with Loongmen-Neo, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lizi-cl/loongmen-neo
   cd loongmen-neo
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Weaviate**:
   - Ensure you have a Weaviate instance running. You can set up a local instance or use a cloud service.
   - Update the `weaviate_config.json` file with your Weaviate instance details.

4. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

1. **Input Text**: Provide the text content you want to analyze for potential copyright infringement.
2. **Run Scan**: The tool will process the text, generate embeddings, and perform a similarity search using Weaviate.
3. **Review Results**: Examine the generated report to identify matching content and assess potential infringements.

## Configuration

Loongmen-Neo can be customized to suit your specific needs. Key configuration options include:

- **Embedding Model**: Choose from a variety of pre-trained embedding models or train your own.
- **Weaviate Schema**: Define the schema in Weaviate to optimize the search process for your dataset.
- **Thresholds**: Adjust similarity thresholds to control the sensitivity of the infringement detection.

## Contributing

We welcome contributions from the community! If you'd like to contribute to Loongmen-Neo, please follow these steps:

1. **Fork the Repository**: Create a fork of the repository on GitHub.
2. **Create a Branch**: Make your changes in a new branch.
3. **Submit a Pull Request**: Once your changes are ready, submit a pull request with a detailed description of your modifications.

## License

Loongmen-Neo is released under the Apache 2.0 License. See the `LICENSE` file for more details.

## Support

For any questions, issues, or feature requests, please open an issue on the GitHub repository or contact the maintainers directly.

## Acknowledgments

We would like to thank the developers of Weaviate and the open-source community for their invaluable contributions to the tools and libraries that make Loongmen-Neo possible.

---

Thank you for using Loongmen-Neo! We hope this tool helps you protect your intellectual property and maintain the integrity of your content.