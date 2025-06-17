# Vidu MCP 使用指南

## 概述

Vidu MCP 是一个允许您通过支持 Model Context Protocol (MCP) 的应用程序（如 Claude 或 Cursor）访问 Vidu 最新视频生成模型的工具。通过这个集成，您可以随时随地生成高质量视频，包括文本到视频、图像到视频等多种转换方式。

[English Version](https://github.com/shengshu-ai/vidu-mcp/blob/main/README.md)

## 主要功能

* **文本生成视频**：使用文字提示生成创意视频
* **图像生成视频**：使用文字提示生成创意视频
* **参考生成视频**：使用文字提示生成创意视频
* **首尾帧生成视频**：使用文字提示生成创意视频

## 系统组件

该系统的主要组件：

1. **UVX MCP 服务器**：
   - 基于 Python 的云端服务器
   - 直接与 Vidu API 通信
   - 提供完整的视频生成功能

## 安装与配置

### 前提条件

1. **Python 3.10 或更新版本**
2. **UV/UVX**
3. **Vidu API 密钥**：从 [Vidu Platform](https://platform.vidu.cn) 获取 (API Credits 需要从[Vidu Platform](https://platform.vidu.cn)购买)

### 获取依赖

1. **Python**：
   - 从 [Python 官网](https://www.python.org/downloads/) 下载并安装
   - 确保将 Python 添加到系统路径

2. **UV/UVX**
   - 通过下面方式下载UV / UVX
   - mac/linux
     ```
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - Windows
     ```
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

## 如何使用 MCP Server

### 1. 获取 Vidu API 密钥

- 访问 [Vidu Platform](https://platform.vidu.cn)
- 注册/登录您的账户
- 在个人设置中创建并复制您的 API 密钥

### 2. 下载必要依赖

- **Python**：安装 Python 3.10 或更高版本
- **UV/UVX**：安装最新稳定版的 UV & UVX

### 3. 配置 MCP 客户端

- 打开您的 MCP 客户端（如 Claude for Desktop 或 Cursor）
- 找到客户端设置
- 找到并打开 `mcp_config.json` 文件（或相应的配置文件）
- 根据您选择的方式添加配置：

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

- 保存配置文件

### 4. 重启 MCP 客户端或刷新 MCP 服务器

- 完全关闭并重新打开您的 MCP 客户端
- 或者，如果客户端支持，使用刷新 MCP 服务器选项

## 具体客户端配置

### Claude for Desktop 配置

1. 打开 Claude 应用
2. 转到 Claude > 设置 > 开发者 > 编辑配置
3. 打开 `claude_desktop_config.json` 文件
4. 添加上述配置并保存
5. 重启 Claude 应用
   - 如果连接成功, 首页不会提示任何error, 且mcp设置亮绿灯
   - 如果连接失败, 首页会提示连接失败

### Cursor 配置

1. 打开 Cursor 应用
2. 转到设置 > Model Context Protocol
3. 添加新服务器
4. 填写服务器详情（与上面 JSON 配置中的信息相同）
5. 保存并重启 or 刷新mcp server

## 使用方法

### 文生视频

通过 Claude 或 Cursor，您可以使用自然语言描述要生成的视频：

**基础示例**：

```
以浅蓝色和淡琥珀色为基调的超写实时尚摄影风格，一位身着宇航服的宇航员在雾中穿行。背景由迷人的白色和金色灯光组成，营造出极简主义的静物画和令人印象深刻的全景场景。
```

**进阶示例（带参数）**：
```
使用以下参数生成夜间城市景观视频：
提示：夜空下摩天大楼灯光闪烁，汽车灯光在道路上形成光带
模型：viduq1
风格：普通
时长：5 秒
宽高比：16:9
分辨率：1080p
运动幅度：中等
```

## 常见问题

**如何获取 Vidu API 密钥？**
- 访问 [Vidu Platform](https://platform.vidu.cn)，注册账户后在API-KEY 中生成 API 密钥。

**服务器不响应怎么办？**
1. 检查您的 API 密钥是否有效
2. 查看错误日志（通常在 Claude 或 Cursor 的日志文件夹中）

**如何获取积分呢？**
- 如尚未在 API 平台完成充值，请先前往充值。直达链接：[Vidu Platform](https://platform.vidu.cn/billing)

**生成的视频在哪里？**
- 生成的视频会通过 URL 链接提供，您可以点击链接查看、下载或分享视频。

**视频生成需要多长时间？**
- 根据视频复杂度、服务器负载和网络状况，通常需要 30 秒到 5 分钟不等。

**如果遇到spawn uvx ENOENT 问题，怎么解决？**
- 此类问题主要是安装uvx/uv path导致，可以通过以下方式解决

Mac/Linux
```
sudo cp ./uvx /usr/local/bin
```

Windows
1. 首先了解安装的 uv/uvx 在哪个位置，在终端输入
   ```
   where uvx
   ```
2. 打开文件管理器，找到uvx/uv文件
3. 放到 C:\Program Files (x86) , C:\Program Files

## 支持

### 技术支持

如果您遇到任何问题或需要帮助，请通过以下方式联系我们：
- 电子邮件: [platform@vidu.studio](mailto:platform@vidu.studio)
- 官方网站: [https://platform.vidu.cn](https://platform.vidu.cn)
