import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings

load_dotenv()

async def main():
    print("Testing Azure OpenAI Connection...")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")

    print(f"Endpoint: {endpoint}")
    print(f"Deployment: {deployment_name}")
    # Don't print full key, just first few chars
    print(f"API Key: {api_key[:5]}..." if api_key else "API Key: None")

    try:
        service = AzureChatCompletion(
            service_id="test",
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version="2025-01-01-preview"
        )
        print("Service object created.")
        
        # Simple completion test
        # We need a kernel to pass to get_chat_message_content? No, actually we can use it directly usually, 
        # but let's see if we can just instantiate it to check creds validation.
        # Ideally we make a call.
        
        from semantic_kernel.contents import ChatHistory
        history = ChatHistory()
        history.add_user_message("Hello")
        
        print("Sending request...")
        # Note: In new SK, get_chat_message_content might require settings
        settings = AzureChatPromptExecutionSettings(service_id="test")
        
        result = await service.get_chat_message_content(
            chat_history=history,
            settings=settings
        )
        print(f"Success! Response: {result}")

    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
