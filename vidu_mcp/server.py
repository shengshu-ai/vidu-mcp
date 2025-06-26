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
    
     Args:
        model (str, required): The model to use. Values range ["viduq1","vidu1.5"], with "viduq1" being the default.
        prompt (str, required): A textual description for video generation, with a maximum length of 1500 characters
        style (str, optional): The style of output video. Defaults to general, Accepted values: general anime
        duration (int, optional): Video duration. Default values vary by model:
                                  - viduq1: default 5s, available: 5
                                  - vidu1.5: default 4s, available: 4, 8
        seed (int, optional): Random seed
                              - Defaults to a random seed number
                              - Manually set values will override the default random seed
        aspect_ratio (str, optional): The aspect ratio of the output video. Values range ["1:1", "16:9","9:16"], with "16:9" being the default.
        resolution (str, optional): Resolution. Default values vary by model & duration:
                                    - viduq1 (5s): default 1080p, available: 1080p
                                    - vidu1.5 (4s): default 360p, available: 360p, 720p, 1080p
                                    - vidu1.5 (8s): default 720p, available: 720p
        movement_amplitude (str, optional): The movement amplitude of objects in the frame.Defaults to auto, accepted value: auto small medium large
        bgm (bool, optional): Whether to add background music to the generated video.
                              - Default: false. Acceptable values: true, false.
                              - When true, the system will automatically add a suitable BGM.
                              - Only when the final generated video duration is 4 seconds is adding BGM supported.
    Returns:
        task_id and video_url
    """
)
def generate_text_to_video(
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
    
    Args:
        image (str, required): An image to be used as the start frame of the generated video
        model (str, required): The model to use. Values range ["viduq1","vidu1.5","vidu2.0"], with "viduq1" being the default.
        prompt (str, optional): A textual description for video generation, with a maximum length of 1500 characters
        duration (int, optional): Video duration. Default values vary by model:
                                  - viduq1: default 5s, available: 5
                                  - vidu2.0 and vidu1.5: default 4s, available: 4, 8
        seed (int, optional): Random seed
                              - Defaults to a random seed number
                              - Manually set values will override the default random seed
        resolution (str, optional): Resolution. Default values vary by model & duration:
                                    - viduq1 (5s): default 1080p, available: 1080p
                                    - vidu2.0 and vidu1.5 (4s): default 360p, options: 360p, 720p, 1080p
                                    - vidu2.0 and vidu1.5 (8s): default 720p, options: 720p
        movement_amplitude (str, optional): The movement amplitude of objects in the frame.Defaults to auto, accepted value: auto small medium large
        bgm (bool, optional): Whether to add background music to the generated video.
                              - Default: false. Acceptable values: true, false.
                              - When true, the system will automatically add a suitable BGM.
                              - Only when the final generated video duration is 4 seconds is adding BGM supported.
    Returns:
        task_id and video_url
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
    
    Args:
        images (str list, required): The model will use the provided images as references to generate a video with consistent subjects
                                     For fields that accept images:
                                     -Accepts 1 to 3 images.
        prompt (str, required): A textual description for video generation, with a maximum length of 1500 characters
        model (str, required): The model to use. Values range ["vidu1.5","vidu2.0"], with "vidu2.0" being the default.
        duration (int, optional): Video duration parameter, with default values depending on the model:
                                  - vidu2.0: Default is 4 seconds, available option: 4
                                  - vidu1.5: Default is 4 seconds, available options: 4, 8
        seed (int, optional): Random seed
                              - Defaults to a random seed number
                              - Manually set values will override the default random seed
        aspect_ratio (str, optional): The aspect ratio of the output video. Defaults to 16:9, accepted: 16:9 9:16 1:1
        resolution (str, optional): The resolution of the output video
                                    Defaults to 360p , accepted value: 360p 720p 1080p
                                    - Model vidu1.5 duration 4 accepted: 360p 720p 1080p
                                    - Model vidu1.5 duration 8accepted: 720p
                                    - Model vidu2.0 duration 4 accepted: 360p 720p
        movement_amplitude (str, optional): The movement amplitude of objects in the frame.Defaults to auto, accepted value: auto small medium large
        bgm (bool, optional): Whether to add background music to the generated video.
                              - Default: false. Acceptable values: true, false.
                              - When true, the system will automatically add a suitable BGM.
                              - Only when the final generated video duration is 4 seconds is adding BGM supported.
    Returns:
        task_id and video_url
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
    Args:
        images (str list, required): Two images: first is start frame, second is end frame.
        model (str, required): The model to use. Values range ["vidu1.5","vidu2.0","viduq1-classic","viduq1"], with "viduq1" being the default.
        prompt (str, optional): A textual description for video generation, with a maximum length of 1500 characters
        duration (int, optional): Video duration. Default values vary by model:
                                  - viduq1 and viduq1-classic: default 5s, available: 5
                                  - vidu2.0 and vidu1.5: default 4s, available: 4, 8
        seed (int, optional): Random seed
                              - Defaults to a random seed number
                              - Manually set values will override the default random seed
        resolution (str, optional): Resolution (based on model & duration):
                                    - viduq1 and viduq1-classic(5s): default 1080p, options: 1080p
                                    - vidu2.0 and vidu1.5 (4s): default 360p, options: 360p, 720p, 1080p
                                    - vidu2.0 and vidu1.5 (8s): default 720p, options: 720p
        movement_amplitude (str, optional): The movement amplitude of objects in the frame.Defaults to auto, accepted value: auto small medium large
        bgm (bool, optional): Whether to add background music to the generated video.
                              - Default: false. Acceptable values: true, false.
                              - When true, the system will automatically add a suitable BGM.
                              - Only when the final generated video duration is 4 seconds is adding BGM supported.
    Returns:
        task_id and video_url
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


@mcp.tool(
    description="""Generate a video from a template.

    COST WARNING: This tool makes an API call to Vidu which may incur costs. Only use when explicitly requested by the user.

    Args:
        template (str, required): AI video template. Different templates have different call parameters.
        images (str list, required): Images
        prompt (str, optional): A textual description for video generation, with a maximum length of 1500 characters
        seed (int, optional): Random seed
                              - Defaults to a random seed number
                              - Manually set values will override the default random seed
        aspect_ratio (str, optional): The aspect ratio of the output video. Defaults to 16:9, accepted: 16:9 9:16 1:1
                                       - Different templates accepted different aspect ratio
        area (str, optional): Exotic Princess style control field only for template exotic_princess,
                              Default：auto, accepts：denmark,uk,africa,china,mexico,switzerland,russia,italy,korea,thailand,india,japan
        beast (str, optional): beast companion style control field only for template beast_companion，
                               Default auto, accepts：bear,tiger,elk,snake,lion,wolf
        bgm (bool, optional): Whether to add background music to the generated video.
                              - Default: false. Acceptable values: true, false.
                              - When true, the system will automatically add a suitable BGM.
                              - Only when the final generated video duration is 4 seconds is adding BGM supported.
    Returns:
        task_id and video_url
    """
)
def generate_template_to_video(
        template: str,
        images: list[str],
        prompt: str = "",
        seed: int = 0,
        aspect_ratio: str = "",
        area: str = "auto",
        beast: str = "auto",
        bgm: bool = False,
) -> str:
    try:
        if not template:
            raise ViduRequestError("template is required")
        if not images:
            raise ViduRequestError("images is required")

        input_images = del_input_images(images)

        # step1: submit video generation task
        payload = {
            "template": template,
            "images": input_images,
            "prompt": prompt,
            "seed": seed,
            "aspect_ratio": aspect_ratio,
            "bgm": bgm,
        }
        if template is "exotic_princess":
            payload["area"] = area
        if template is "beast_companion":
            payload["beast"] = beast

        response_data = api_client.post("/ent/v2/template2video", json=payload)
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
