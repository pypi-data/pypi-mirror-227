# nonebot-plugin-groupAccountant

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/shilapi/nonebot-plugin-groupAccountant.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-example">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-groupAccountant.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

## 📖 介绍

Nonebot 群记账插件

通过群消息记录开销，并保存在json文件中，可通过群消息读取

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-groupAccountant

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-groupAccountant
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-groupAccountant
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-groupAccountant
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-groupAccountant
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_groupAccountant"]

</details>

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 记账 | 群员 | 否 | 私聊 | /记账 [开销名] [人数] [金额] |
| 清算 | 群员 | 是 | 群聊 | /清算 [clear] (可选，用于清空账本) |
### 效果图
![效果](images/img1.png)
