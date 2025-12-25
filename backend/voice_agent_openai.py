import logging
import os
import ssl
import sys
import warnings
from pathlib import Path

# Suppress Pydantic warning about validate_default
warnings.filterwarnings("ignore", message=".*validate_default.*")

try:
    import certifi
except ImportError:
    certifi = None
from dotenv import load_dotenv

from livekit.agents import JobContext, JobProcess, WorkerOptions, cli
from livekit.agents.job import AutoSubscribe
from livekit.agents.llm import ChatContext
# from livekit.agents.pipeline import VoicePipelineAgent # Removed in 1.0
from livekit.plugins import cartesia, deepgram, silero, openai

from llama_index.llms.openai_like import OpenAILike
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    Settings,
)
from llama_index.core.chat_engine.types import ChatMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Load environment variables
load_dotenv()

# Fix SSL certificate issue on Windows
if certifi:
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# Configure logging with more detail for debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("voice-assistant")

# ============================================
# Environment Variable Validation
# ============================================
def validate_env_vars():
    """Validate all required environment variables at startup."""
    errors = []
    warnings_list = []
    
    # Required API Keys
    required_vars = {
        'OPENROUTER_API_KEY': 'OpenRouter API for LLM',
        'LIVEKIT_URL': 'LiveKit server URL',
        'LIVEKIT_API_KEY': 'LiveKit API key',
        'LIVEKIT_API_SECRET': 'LiveKit API secret',
        'DEEPGRAM_API_KEY': 'Deepgram speech-to-text',
        'CARTESIA_API_KEY': 'Cartesia text-to-speech',
    }
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            errors.append(f"  - {var}: {description}")
        elif value.startswith('your_') or value == '':
            warnings_list.append(f"  - {var}: appears to be a placeholder value")
    
    # Validate LiveKit URL format
    livekit_url = os.getenv('LIVEKIT_URL', '')
    if livekit_url and not (livekit_url.startswith('wss://') or livekit_url.startswith('ws://')):
        errors.append(f"  - LIVEKIT_URL: must start with 'wss://' or 'ws://' (got: {livekit_url[:20]}...)")
    
    if errors:
        logger.error("=" * 60)
        logger.error("CONFIGURATION ERROR: Missing required environment variables")
        logger.error("=" * 60)
        logger.error("Please set the following in your .env file:")
        for err in errors:
            logger.error(err)
        logger.error("")
        logger.error("Example .env file:")
        logger.error("  OPENROUTER_API_KEY=sk-or-...")
        logger.error("  LIVEKIT_URL=wss://your-project.livekit.cloud")
        logger.error("  LIVEKIT_API_KEY=API...")
        logger.error("  LIVEKIT_API_SECRET=...")
        logger.error("  DEEPGRAM_API_KEY=...")
        logger.error("  CARTESIA_API_KEY=...")
        logger.error("=" * 60)
        sys.exit(1)
    
    if warnings_list:
        logger.warning("Potential configuration issues:")
        for warn in warnings_list:
            logger.warning(warn)
    
    return True

# Run validation
validate_env_vars()

# --- Configuration ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CARTESIA_VOICE_ID = os.getenv("CARTESIA_VOICE_ID", "bf0a246a-8642-498a-9950-80c35e9276b5")

# Resolve paths relative to this file
CURRENT_DIR = Path(__file__).parent
PERSIST_DIR = CURRENT_DIR / "../chat-engine-storage"
DOCS_DIR = CURRENT_DIR / "../docs"

# Validate docs directory exists
if not DOCS_DIR.exists():
    logger.warning(f"Docs directory not found at {DOCS_DIR}. Creating empty directory.")
    DOCS_DIR.mkdir(parents=True, exist_ok=True)


# Configure Models
logger.info("Loading embedding model...")
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
logger.info("Embedding model loaded.")
llm = OpenAILike(
    model="openai/gpt-4o-mini",
    api_base="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    is_chat_model=True,
)
Settings.llm = llm
Settings.embed_model = embed_model

# check if storage already exists
if not PERSIST_DIR.exists():
    logger.info(f"Creating new index from documents in '{DOCS_DIR}'...")
    # load the documents and create the index
    if not DOCS_DIR.exists():
        logger.error(f"Docs directory not found at {DOCS_DIR}")
        sys.exit(1)
        
    documents = SimpleDirectoryReader(str(DOCS_DIR)).load_data()
    logger.info(f"Loaded {len(documents)} documents.")
    index = VectorStoreIndex.from_documents(documents)
    logger.info("Index created.")
    # store it for later
    index.storage_context.persist(persist_dir=str(PERSIST_DIR))
    logger.info("Index persisted to storage.")
else:
    logger.info("Loading existing index from storage...")
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=str(PERSIST_DIR))
    index = load_index_from_storage(storage_context)
    logger.info("Index loaded.")


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.vad.VAD.load()


async def entrypoint(ctx: JobContext):
    logger.info(f"Entrypoint triggered for room {ctx.room.name}")

    # Create chat context and add system message
    chat_context = ChatContext()
    chat_context.add_message(
        role="system",
        content="You are a funny, witty assistant. Respond with short and concise answers. Avoid using unpronouncable punctuation or emojis."
    )
    
    chat_engine = index.as_chat_engine(chat_mode=ChatMode.CONTEXT)

    logger.info(f"Connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()
    logger.info(f"Starting voice assistant for participant {participant.identity}")

    # LiveKit Agents 1.2+ uses Agent + AgentSession
    from livekit.agents.voice import Agent as VoiceAgent, AgentSession

    # Agent has instructions and chat_ctx
    agent = VoiceAgent(
        instructions="You are a funny, witty assistant. Respond with short and concise answers. Avoid using unpronouncable punctuation or emojis.",
        chat_ctx=chat_context,
    )

    # AgentSession handles the audio components
    # Use OpenAI plugin with OpenRouter as base URL
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(),
        llm=openai.LLM(
            model="openai/gpt-4o-mini",
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        ),
        tts=cartesia.TTS(
            model="sonic-2",
            voice=CARTESIA_VOICE_ID,
        ),
    )

    # Start the session (returns RunResult or None)
    await session.start(agent, room=ctx.room)
    
    logger.info("Agent session started, sending greeting...")
    await session.say(
        "Hey there! How can I help you today?",
        allow_interruptions=True,
    )


if __name__ == "__main__":
    logger.info("Starting voice agent...")
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )