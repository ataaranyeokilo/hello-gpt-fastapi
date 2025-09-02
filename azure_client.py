# azure_client.py
from openai import AzureOpenAI
from openai import (  # exception types
    APIError, RateLimitError, APITimeoutError, APIConnectionError,
    AuthenticationError, BadRequestError, OpenAIError
)
import config
import time
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_client() -> AzureOpenAI:
    """Create the Azure OpenAI client on first use (cached thereafter)."""
    return AzureOpenAI(
        api_key=config.AZURE_OPENAI_KEY,
        api_version=config.AZURE_OPENAI_API_VERSION,
        azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    )

def ask_gpt(question: str, *, timeout: float = 20.0, max_retries: int = 2) -> str:
    """
    Send a question to Azure OpenAI with simple retries and timeouts.
    Raises RuntimeError with a user-friendly message on failure.
    """
    q = (question or "").strip()
    if not q:
        raise RuntimeError("Question is empty.")

    attempt = 0
    backoff = 1.5

    while True:
        attempt += 1
        try:
            # Lazy init happens here:
            client = get_client()

            resp = client.chat.completions.create(
                model=config.AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": q},
                ],
                max_tokens=400,
                timeout=timeout,  # request-level timeout (seconds)
            )
            return resp.choices[0].message.content

        except (APITimeoutError, APIConnectionError) as e:
            logger.warning(f"[ask_gpt] network/timeout (attempt {attempt}): {e}")
            if attempt <= max_retries:
                time.sleep(backoff ** attempt)
                continue
            raise RuntimeError("Azure OpenAI is timing out. Please try again.")

        except RateLimitError as e:
            logger.warning(f"[ask_gpt] rate limited (attempt {attempt}): {e}")
            if attempt <= max_retries:
                time.sleep(backoff ** attempt)
                continue
            raise RuntimeError("We’re being rate-limited. Try again in a moment.")

        except AuthenticationError:
            logger.exception("[ask_gpt] bad API key / auth")
            raise RuntimeError("Authentication failed. Check your API key.")

        except BadRequestError as e:
            logger.exception(f"[ask_gpt] bad request: {e}")
            raise RuntimeError("Your request was rejected by the model.")

        except APIError as e:
            logger.exception(f"[ask_gpt] generic API error: {e}")
            raise RuntimeError("Azure OpenAI error occurred. Please try again.")

        except OpenAIError as e:
            # Covers constructor/config issues, etc.
            logger.exception(f"[ask_gpt] OpenAI SDK error: {e}")
            raise RuntimeError("Azure OpenAI client is misconfigured. Check endpoint, key, and deployment.")

        except Exception as e:
            logger.exception(f"[ask_gpt] unexpected error: {e}")
            raise RuntimeError("Unexpected error. Please try again.")
