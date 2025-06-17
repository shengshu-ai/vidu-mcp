# Vidu MCP

A tool that allows you to access Vidu latest video generation models via applications that support the Model Context Protocol (MCP), such as Claude or Cursor.

[中文文档](https://github.com/shengshu-ai/vidu-mcp/blob/main/README-CN.md)


## Overview

Vidu MCP is a tool that allows you to access Vidu latest video generation models via applications that support the Model Context Protocol (MCP), such as Claude or Cursor. This integration enables you to generate high-quality videos anytime, anywhere — including text-to-video, image-to-video, and more.

## Key Features

- **Text-to-Video Generation**: Generate creative videos using text prompts
- **Image-to-Video Generation**: Generate creative videos using text and image prompts
- **Reference-to-Video Generation**: Generate creative videos using text and image prompts
- **StartEnd-to-Video Generation**: Generate creative videos using text and image prompts


## System Components

The system consists of two main components:

1. **UVX MCP Server**
   - Python-based cloud server
   - Communicates directly with the Vidu API
   - Provides full video generation capabilities

## Installation & Configuration

### Prerequisites

1. Python 3.10 or higher
2. UV/UVX
3. Vidu API Key: Obtain from Vidu Platform (This feature requires API Credits, which must be purchased separately on [Vidu Platform](https://platform.vidu.com/)


### Get Dependencies

1. **Python**:
   - Download and install from the official Python website
   - Ensure Python is added to your system path

2. **UV/UVX**:
   - Install uv and set up our Python project and environment:

#### Mac/Linux
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## How to Use MCP Server

### 1. Get Vidu API Key
- Visit the [Vidu Platform](https://platform.vidu.com/)
- Register or log into your account
- Create and copy your API key from the account settings

### 2. Download Required Dependencies
- **Python**: Install Python 3.10 or above
- **UV/UVX**: Install the latest stable version of UV & UVX

### 3. Configure MCP Client
- Open your MCP client (e.g., Claude for Desktop or Cursor)
- Locate the client settings
- Open mcp_config.json (or relevant config file)
- Add the configuration based on the method you use:

```json
{
  "mcpServers": {
    "Vidu": {
      "command": "uvx",
      "args": [
        "vidu-mcp"
      ],
      "env": {
        "VIDU_API_KEY": "api-key-here", 
        "VIDU_API_HOST": "api-host-here"
      }
    }
  }
}
```

- Save the config file

### 4. Restart MCP Client or Refresh MCP Server
- Fully close and reopen your MCP client
- Or use the "Refresh MCP Server" option if supported

## Client-specific Configuration

### Claude for Desktop

1. Open the Claude application
2. Navigate to Claude > Settings > Developer > Edit Config
3. Open the claude_desktop_config.json file
   - Windows
   - Mac : ~/Library/Application\ Support/Claude/claude_desktop_config.json
4. Add the configuration above and save
5. Restart Claude
   - If connected successfully: the homepage will not show any error and the MCP status will be green
   - If connection fails: an error message will be shown on the homepage

### Cursor

1. Open the Cursor application
2. Go to Settings > Model Context Protocol
3. Add a new server
4. Fill in the server details as in the JSON config above
5. Save and restart or refresh the MCP server

## Usage Examples

### Text-to-Video

Use natural language prompts via Claude or Cursor to generate videos.

**Basic Example**:
```
In an ultra-realistic fashion photography style featuring light blue and pale amber tones, an astronaut in a spacesuit walks through the fog. The background consists of enchanting white and golden lights, creating a minimalist still life and an impressive panoramic scene.
```

**Advanced Example with Parameters**:
```
Generate a night cityscape video with the following parameters:
Prompt: Skyscraper lights twinkling under the night sky, with car lights forming streaks on the road
Model: viduq1
Style: general
Duration: 5 seconds
Aspect Ratio: 16:9
Resolution: 1080p
Movement Amplitude: middle
```

## FAQ

**How do I get a Vidu API key?**
- Register at the Vidu Platform and generate it under "API-KEY" in your account.

**What should I do if the server doesn't respond?**
1. Check whether your API key is valid
2. View error logs (typically in the log folders of Claude or Cursor)

**How to obtain credits?**
- If you haven't topped up on the API platform yet, please do so first. [Vidu Platform](https://platform.vidu.com/billing)

**Where can I find the generated video?**
- You will receive a URL link to view, download, or share the video.

**How long does video generation take?**
- Typically 30 seconds to 5 minutes depending on complexity, server load, and network conditions.

**What to do if you encounter a spawn uvx ENOENT error?**
- This error is typically caused by incorrect UV/UVX installation paths. You can resolve it as follows:

For Mac/Linux:
```
sudo cp ./uvx /usr/local/bin
```

For Windows:
1. Identify the installation path of UV/UVX by running the following command in the terminal:
```
where uvx
```
2. Open File Explorer and locate the uvx/uv files.
3. Move the files to one of the following directories:
   - C:\Program Files (x86) or C:\Program Files

## Support
### Technical Support
- Email: [platform@vidu.studio](mailto:platform@vidu.studio)
- Website: [https://platform.vidu.com](https://platform.vidu.com)
