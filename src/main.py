import asyncio
import logging
from dotenv import load_dotenv

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    load_dotenv()
    logging.info("Starting Neo-Atom...")
    # TODO: Load LLM agent
    # TODO: Init Listener
    # TODO: Init Speaker
    # TODO: Main interaction loop

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Neo-Atom shut down gracefully by user.")
