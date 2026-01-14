# Azure Blob Storage AI Agent

An intelligent AI agent built with Microsoft Semantic Kernel that reads and analyzes data from Azure Blob Storage based on natural language prompts.

## Features

- 🤖 **Natural Language Interface**: Ask questions about your data in plain English
- ☁️ **Azure Integration**: Seamlessly connects to Azure Blob Storage and Azure OpenAI
- 📊 **Data Analysis**: Automatically reads and formats CSV data from blob storage
- 🔧 **Extensible Plugin System**: Built on Semantic Kernel's plugin architecture

## Prerequisites

- Python 3.8 or higher
- Azure Blob Storage account
- Azure OpenAI resource with a deployed model (e.g., `gpt-4o-mini`)

## Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   
   Create or update the `.env` file with your Azure credentials:
   ```env
   # Azure Blob Storage Credentials
   AZURE_STORAGE_ACCOUNT_NAME=your-storage-account-name
   AZURE_STORAGE_ACCOUNT_KEY=your-storage-account-key
   AZURE_STORAGE_CONTAINER_NAME=your-container-name

   # Azure OpenAI Credentials
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
   ```

   > ⚠️ **Important**: 
   > - The endpoint should be the base URL only (not the full API path)
   > - Keep your API keys secure and never commit them to version control

## Usage

### Running the Agent

Start the interactive agent:
```bash
python blob_agent.py
```

### Example Queries

Once the agent is running, you can ask questions like:

- `"List all files in the storage."`
- `"Read the sales data file and show me the first 5 records."`
- `"What are the columns in the CSV file?"`
- `"Show me the data from csv-data/sales_data.csv"`

### Exiting

Type `exit` or `quit` to stop the agent.

## Project Structure

```
.
├── blob_agent.py          # Main agent script
├── test_openai.py         # Connectivity test script
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration (not in git)
└── README.md             # This file
```

## How It Works

1. **Semantic Kernel Framework**: The agent uses Microsoft's Semantic Kernel to orchestrate AI interactions
2. **Plugin Architecture**: A custom `BlobStoragePlugin` provides two functions:
   - `read_csv_blob`: Downloads and previews CSV files from blob storage
   - `list_blobs`: Lists all files in the configured container
3. **Auto Function Calling**: The AI automatically determines when to call these functions based on your questions
4. **Natural Language Response**: Results are formatted and presented in a conversational manner

## Troubleshooting

### Authentication Errors (401)

- **Issue**: `Access denied due to invalid subscription key`
- **Solution**: Verify your `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` in the `.env` file

### Missing Dependencies

- **Issue**: `ModuleNotFoundError` or `ImportError`
- **Solution**: Run `pip install -r requirements.txt`

### Blob Not Found

- **Issue**: `Blob does not exist in container`
- **Solution**: 
  - Verify the blob path (e.g., `csv-data/sales_data.csv`)
  - Check your `AZURE_STORAGE_CONTAINER_NAME` is correct
  - Use the `list_blobs` function to see available files

### Testing Connectivity

Run the test script to verify your Azure OpenAI connection:
```bash
python test_openai.py
```

## Dependencies

- `semantic-kernel` - Microsoft Semantic Kernel framework
- `azure-storage-blob` - Azure Blob Storage SDK
- `python-dotenv` - Environment variable management
- `pandas` - Data manipulation and analysis
- `tabulate` - Table formatting for markdown output

## Security Best Practices

- ✅ Store credentials in `.env` file (already in `.gitignore`)
- ✅ Use Azure Key Vault for production deployments
- ✅ Rotate API keys regularly
- ✅ Use managed identities when running in Azure

## License

This project is for internal use.

## Support

For issues or questions, please contact the development team.
