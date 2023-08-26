# 有趣

> 有趣，是一个使用简单且功能强大的自动化测试基础框架。

![PyPI](https://img.shields.io/pypi/v/youqu?style=flat&logo=github&link=https%3A%2F%2Fpypi.org%2Fproject%2Fyouqu%2F)
![PyPI - License](https://img.shields.io/pypi/l/youqu)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/youqu)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/youqu)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/youqu)

[![Downloads](https://static.pepy.tech/badge/youqu/week)](https://pepy.tech/project/youqu)
[![Downloads](https://static.pepy.tech/badge/youqu/month)](https://pepy.tech/project/youqu)
[![Downloads](https://static.pepy.tech/badge/youqu)](https://pepy.tech/project/youqu)

[English](README.md) | 简体中文

有趣（YouQu） 是一个自动化测试基础框架（AutoTest Basic Frame），基于业内流行的自动化测试框架 Pytest 进行封装编写，支持对用例进行方便的编写、组织、执行，核心库包括：OpenCV、Dogtail、OCR 等、及多个自研自动化测试组件，提供灵活的执行配置、用例标签化管理等特色功能。

## 安装

- 从 PyPI 安装:

  ```shel
  sudo pip3 install youqu
  ```

  创建项目:

  ```shell
  youqu-startproject my_project
  ```

  安装依赖:

  ```sh
  cd my_project
  bash env.sh
  ```

- 从源码安装:

  ```sh
  git clone https://github.com/linuxdeepin/deepin-autotest-framework.git my_project
  cd my_project
  bash env.sh
  ```

### 使用

```sh
youqu manage.py run
```

## 文档

- [文档](https://mikigo.github.io/youqu-docs/)

## 帮助

- [官方论坛](https://bbs.deepin.org/) 
- [开发者中心](https://github.com/linuxdeepin/developer-center) 
- [Wiki](https://wiki.deepin.org/)

## 贡献指南

我们鼓励您报告问题并做出更改

- [开发者代码贡献指南](https://github.com/linuxdeepin/developer-center/wiki/Contribution-Guidelines-for-Developers) 

## 开源许可证

有趣 在 [GPL-2.0-only](LICENSE) 下发布。