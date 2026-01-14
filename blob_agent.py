import asyncio
import os
import io
import pandas as pd
from typing import Annotated
from dotenv import load_dotenv

# Semantic Kernel imports
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments

# Azure Blob imports
from azure.storage.blob import BlobServiceClient

# Load environment variables
load_dotenv()

class BlobStoragePlugin:
    """
    A Semantic Kernel plugin to interact with Azure Blob Storage.
    """
    
    def __init__(self):
        self.account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        self.account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        
        if not all([self.account_name, self.account_key, self.container_name]):
            raise ValueError("Azure Blob Storage credentials are missing in .env file.")

        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{self.account_name}.blob.core.windows.net",
            credential=self.account_key
        )
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
    
    @kernel_function(
        description="Reads the content of a CSV file from Azure Blob Storage and returns a preview.",
        name="read_csv_blob"
    )
    def read_csv_blob(
        self,
        blob_name: Annotated[str, "The name of the blob file to read (e.g., 'csv-data/sales_data.csv')."]
    ) -> Annotated[str, "A string representation of the first few rows of the CSV file."]:
        """
        Downloads a CSV blob and returns the first 10 rows.
        """
        try:
            print(f"\n[Tool] Downloading blob: {blob_name}...")
            blob_client = self.container_client.get_blob_client(blob_name)
            
            if not blob_client.exists():
                return f"Error: Blob '{blob_name}' does not exist in container '{self.container_name}'."
            
            blob_data = blob_client.download_blob().readall()
            df = pd.read_csv(io.BytesIO(blob_data))
            
            # Return a markdown formatted table or string representation
            return df.head(10).to_markdown()
        except Exception as e:
            return f"Error reading blob: {str(e)}"

    @kernel_function(
        description="Lists all blobs in the configured container.",
        name="list_blobs"
    )
    def list_blobs(self) -> Annotated[str, "A list of blob names in the container."]:
        """
        Lists all blobs in the container.
        """
        try:
            blobs = self.container_client.list_blobs()
            blob_names = [b.name for b in blobs]
            return ", ".join(blob_names) if blob_names else "No blobs found."
        except Exception as e:
            return f"Error listing blobs: {str(e)}"

async def main():
    # 1. Initialize Kernel
    kernel = Kernel()

    # 2. Configure Azure OpenAI Service
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")

    if not all([deployment_name, endpoint, api_key]):
        print("Missing Azure OpenAI credentials in .env file. Please configure them.")
        return

    service_id = "chat-gpt"
    kernel.add_service(
        AzureChatCompletion(
            service_id=service_id,
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version="2025-01-01-preview"
        )
    )

    # 3. Import Plugin
    try:
        kernel.add_plugin(BlobStoragePlugin(), plugin_name="BlobTools")
    except Exception as e:
        print(f"Failed to initialize BlobStoragePlugin: {e}")
        return

    # 4. Create Chat History
    history = ChatHistory()
    history.add_system_message("You are an AI assistant that can read data from Azure Blob Storage using the BlobTools plugin. Always check what files are available first if you are unsure.")

    print("--- Azure Blob Storage Agent (Semantic Kernel) ---")
    print("Type 'exit' to quit.\n")

    # 5. Chat Loop
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        history.add_user_message(user_input)

        # Get the chat completion service
        chat_completion = kernel.get_service(type=AzureChatCompletion)
        
        # Enable auto function calling
        execution_settings = AzureChatPromptExecutionSettings(service_id=service_id)
        execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

        try:
            result = await chat_completion.get_chat_message_content(
                chat_history=history,
                settings=execution_settings,
                kernel=kernel
            )
            
            print(f"Agent: {result.content}\n")
            history.add_message(result)
            
        except Exception as e:
            print(f"Error during chat: {e}")

if __name__ == "__main__":
    asyncio.run(main())
