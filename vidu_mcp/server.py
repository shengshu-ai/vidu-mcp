"""
Vidu MCP Server

⚠️ IMPORTANT: This server connects to Vidu API endpoints which may involve costs.
Any tool that makes an API call is clearly marked with a cost warning. Please follow these guidelines:

1. Only use these tools when users specifically ask for them

Note: Tools without cost warnings are free to use as they only read existing data.
"""
import requests
import time
from dotenv import load_dotenv
import json
from mcp.server.fastmcp import FastMCP
import logging
import sys

from vidu_mcp.client import ViduAPIClient
from vidu_mcp.exceptions import ViduAPIError
from vidu_mcp.const import *
from vidu_mcp.util import *

load_dotenv()
api_key = ENV_VIDU_API_KEY
if api_key is None:
    api_key = os.environ.get("VIDU_API_KEY")
api_host = ENV_VIDU_API_HOST
if api_host is None:
    api_host = os.environ.get("VIDU_API_HOST")
fastmcp_log_level = os.getenv(ENV_FASTMCP_LOG_LEVEL) or "WARNING"

if not api_key:
    raise ValueError("VIDU_API_KEY environment variable is required")
if not api_host:
    raise ValueError("VIDU_API_HOST environment variable is required")

logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("vidu-mcp")

mcp = FastMCP("Vidu", log_level=fastmcp_log_level)
api_client = ViduAPIClient(api_key, api_host)


@mcp.tool(
    description="""Generate a video from a prompt.

    COST WARNING: This tool makes an API call to Vidu which may incur costs. Only use when explicitly requested by the user.
    """
)
def generate_text_to_video1(
        model: str = "viduq1",
        prompt: str = "",
        style: str = "general",
        duration: int = 5,
        seed: int = 0,
        aspect_ratio: str = "16:9",
        resolution: str = "1080p",
        movement_amplitude: str = "auto",
        bgm: bool = False,
) -> str:
    try:
        if not prompt:
            raise ViduRequestError("Prompt is required")

        # step1: submit video generation task
        payload = {
            "model": model,
            "style": style,
            "prompt": prompt,
            "duration": duration,
            "seed": seed,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "movement_amplitude": movement_amplitude,
            "bgm": bgm,
        }

        response_data = api_client.post("/ent/v2/text2video", json=payload)
        task_id = response_data.get("task_id")
        if not task_id:
            raise ViduRequestError("Failed to get task_id from response")

        return query_video(task_id=task_id)

    except ViduAPIError as e:
        logger.error(f"Parameter validation error: {str(e)}")
        return f"Error: {str(e)}"
    except (IOError, requests.RequestException) as e:
        logger.error(f"Parameter validation error: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Text-to-video generation error: {str(e)}")
        return f"Error generating video: {str(e)}"


@mcp.tool(
    description="""Generate a video from a pic and prompt.

    COST WARNING: This tool makes an API call to Vidu which may incur costs. Only use when explicitly requested by the user.
    """
)
def generate_img_to_video(
        image: str,
        model: str = "viduq1",
        prompt: str = "",
        duration: int = 5,
        seed: int = 0,
        resolution: str = "1080p",
        movement_amplitude: str = "auto",
        bgm: bool = False,
) -> str:
    try:
        if not image:
            raise ViduRequestError("image is required")

        image = del_input_image(image)

        # step1: submit video generation task
        payload = {
            "model": model,
            "images": [image],
            "prompt": prompt,
            "duration": duration,
            "seed": seed,
            "resolution": resolution,
            "movement_amplitude": movement_amplitude,
            "bgm": bgm,
        }

        response_data = api_client.post("/ent/v2/img2video", json=payload)
        task_id = response_data.get("task_id")
        if not task_id:
            raise ViduRequestError("Failed to get task_id from response")

        return query_video(task_id=task_id)

    except ViduAPIError as e:
        logger.error(f"Parameter validation error: {str(e)}")
        return f"Error: {str(e)}"
    except (IOError, requests.RequestException) as e:
        logger.error(f"Parameter validation error: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Text-to-video generation error: {str(e)}")
        return f"Error generating video: {str(e)}"


@mcp.tool(
    description="""Generate a video from a pic and prompt.

    COST WARNING: This tool makes an API call to Vidu which may incur costs. Only use when explicitly requested by the user.
    """
)
def generate_reference2video_to_video(
        images: list[str],
        prompt: str,
        model: str = "vidu2.0",
        duration: int = 4,
        seed: int = 0,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        movement_amplitude: str = "auto",
        bgm: bool = False,
) -> str:
    try:
        if not images:
            raise ViduRequestError("images is required")
        if not prompt:
            raise ViduRequestError("prompt is required")

        input_images = del_input_images(images)

        # step1: submit video generation task
        payload = {
            "model": model,
            "images": input_images,
            "prompt": prompt,
            "duration": duration,
            "seed": seed,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "movement_amplitude": movement_amplitude,
            "bgm": bgm,
        }

        response_data = api_client.post("/ent/v2/reference2video", json=payload)
        task_id = response_data.get("task_id")
        if not task_id:
            raise ViduRequestError("Failed to get task_id from response")

        return query_video(task_id=task_id)

    except ViduAPIError as e:
        logger.error(f"Parameter validation error: {str(e)}")
        return f"Error: {str(e)}"
    except (IOError, requests.RequestException) as e:
        logger.error(f"Parameter validation error: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Text-to-video generation error: {str(e)}")
        return f"Error generating video: {str(e)}"


@mcp.tool(
    description="""Generate a video from a pic and prompt.

    COST WARNING: This tool makes an API call to Vidu which may incur costs. Only use when explicitly requested by the user.
    """
)
def generate_startend2video_to_video(
        images: list[str],
        model: str = "viduq1",
        prompt: str = "",
        duration: int = 5,
        seed: int = 0,
        resolution: str = "1080p",
        movement_amplitude: str = "auto",
        bgm: bool = False,
) -> str:
    try:
        if not images:
            raise ViduRequestError("images is required")

        input_images = del_input_images(images)

        # step1: submit video generation task
        payload = {
            "model": model,
            "images": input_images,
            "prompt": prompt,
            "duration": duration,
            "seed": seed,
            "resolution": resolution,
            "movement_amplitude": movement_amplitude,
            "bgm": bgm,
        }

        response_data = api_client.post("/ent/v2/start-end2video", json=payload)
        task_id = response_data.get("task_id")
        if not task_id:
            raise ViduRequestError("Failed to get task_id from response")

        return query_video(task_id=task_id)

    except ViduAPIError as e:
        logger.error(f"Parameter validation error: {str(e)}")
        return f"Error: {str(e)}"
    except (IOError, requests.RequestException) as e:
        logger.error(f"Parameter validation error: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Text-to-video generation error: {str(e)}")
        return f"Error generating video: {str(e)}"

def query_video(
        task_id: int,
) -> str:
    try:
        creation_url = None
        max_retries = 30  # 10 minutes total (30 * 20 seconds)
        retry_interval = 20  # seconds

        for attempt in range(max_retries):
            status_response = api_client.get(f"/ent/v2/tasks/{task_id}/creations")
            status = status_response.get("state")

            if status == "failed":
                raise ViduRequestError(f"Video generation failed for task_id: {task_id}")
            elif status == "success":
                creation_url = status_response.get("creations", [{}])[0].get("url")
                if creation_url:
                    break
                raise ViduRequestError(f"Missing creation_url in success response for task_id: {task_id}")

            # Still processing, wait and retry
            time.sleep(retry_interval)

        if not creation_url:
            raise ViduRequestError(f"Failed to get creation_url for task_id: {task_id}")

        # Build result object
        result = {
            "task_id": task_id,
            "status": "success",
            "video_url": creation_url,
        }

        return json.dumps(result, indent=2, ensure_ascii=False)

    except ViduAPIError as e:
        logger.error(f"Parameter validation error: {str(e)}")
        return f"Error: {str(e)}"
    except (IOError, requests.RequestException) as e:
        logger.error(f"Parameter validation error: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Text-to-video generation error: {str(e)}")
        return f"Error generating video: {str(e)}"


def main():
    print("Starting Vidu MCP server")
    """Run the Vidu MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
