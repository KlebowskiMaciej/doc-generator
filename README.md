# 📜 doc-generator

**doc-generator** is a Python-based tool that automatically generates XML documentation comments (e.g., `<summary>`, `<param>`, `<returns>`) for C# code files. It supports two modes of operation:

- **Local Mode**: Uses an offline model (such as Flan-T5) via the Transformers library to parse and document C# classes and methods.
- **Gemini Mode**: When invoked with the `--gemini` flag, the tool sends the entire C# code to the Gemini API (Google Generative AI) and receives back a fully documented version of the code.

## Features

- Automatic generation of XML documentation for classes, methods, enums, structs, interfaces, and fields.
- Dual operation modes: offline (local model) and online (Gemini API).
- Simple command-line interface.
- Configured and managed with Poetry.

## Installation

Ensure you have Python 3.10 or higher installed. Then, clone the repository and install dependencies using Poetry:

```bash
git clone https://github.com/your-username/doc-generator.git
cd doc-generator
poetry build
pip install dist/*.whl
```

## Usage

### Local Mode
By default, doc-generator operates in local mode using an offline model. To generate documentation for your C# file, run:
```bash
doc-generator path/to/YourFile.cs
```
This mode uses a parser and a local language model (e.g., Flan-T5) to generate and insert documentation comments into your code.

### Gemini Mode
To use the Gemini API for documentation generation, supply the --gemini flag. When running in Gemini mode for the first time, you will be prompted for your Gemini API key, which will be saved in your home directory for future use.
```bash
doc-generator path/to/YourFile.cs --gemini
```
In this mode, the entire file content is sent in a single prompt to the Gemini API, which returns the updated code with XML documentation comments inserted.


## Configuration
Key configuration details are managed via the `pyproject.toml` file and the code in the `src` directory:

- **Local Mode Configuration**: Parameters like model name and generation settings are specified in src/config.py.
- **Gemini Mode Configuration**:The Gemini API key is stored in `~/.gemini_config.env`. If the key is missing, the tool will prompt for it.

## Logging
Logging is configured to display messages at the INFO level. All log messages (including those from Gemini interactions) are shown in English.

## Contributing
Contributions, bug reports, and suggestions are welcome! Feel free to open an issue or submit a pull request on GitHub.

## License
This project is licensed under the MIT License.


