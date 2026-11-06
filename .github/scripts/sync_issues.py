#!/usr/bin/env python3
"""把仓库里的 Markdown 文件同步为 GitHub Issue。

旧实现用 `gh issue list --search <标题>` 查重，这是模糊全文检索且只取第一条，
标题相近时会命错 Issue，导致同名 Issue 反复创建。这里改为一次性拉取全部 Issue，
建立「标题 -> 编号」精确索引后再匹配。
"""

import json
import os
import subprocess
import sys

REPO = os.environ.get("GH_REPO") or ""
if not REPO:
    print("缺少 GH_REPO 环境变量")
    sys.exit(1)

ADDED_FILE = "added_modified.txt"
DELETED_FILE = "deleted.txt"


def gh(*args, retry=True):
    """调用 gh CLI，瞬时失败重试一次。"""
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0 and retry:
        print(f"gh {' '.join(args)} 失败，重试一次：{result.stderr.strip()}")
        result = subprocess.run(["gh", *args], capture_output=True, text=True)
    return result


def read_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def build_issue_index():
    """拉取全部 Issue（含已关闭），标题精确映射到编号最小的那条。"""
    listed = gh(
        "api",
        "--paginate",
        f"repos/{REPO}/issues?state=all&per_page=100",
        "--jq",
        "[.[] | select(.pull_request == null) | {number, title, state}]",
    )
    if listed.returncode != 0:
        print(f"拉取 Issue 列表失败：{listed.stderr.strip()}")
        sys.exit(1)

    index = {}
    for line in listed.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            batch = json.loads(line)
        except json.JSONDecodeError:
            continue
        for issue in batch:
            title = issue["title"]
            existing = index.get(title)
            if existing is None or issue["number"] < existing["number"]:
                index[title] = issue
    return index


def sync_one(path, index):
    """处理单个文件，返回 (动作, 是否成功)。"""
    title = os.path.basename(path)
    hit = index.get(title)

    if hit:
        result = gh("issue", "edit", str(hit["number"]), "--body-file", path)
        if result.returncode != 0:
            print(f"  更新失败：{result.stderr.strip()}")
            return "failed", False
        if hit["state"] == "closed":
            gh("issue", "reopen", str(hit["number"]))
        print(f"  更新 #{hit['number']}")
        return "updated", True

    result = gh("issue", "create", "--title", title, "--body-file", path)
    if result.returncode != 0:
        print(f"  创建失败：{result.stderr.strip()}")
        return "failed", False
    print(f"  创建成功：{result.stdout.strip()}")
    return "created", True


def close_one(path, index):
    title = os.path.basename(path)
    hit = index.get(title)
    if not hit or hit["state"] == "closed":
        return "skipped", True

    result = gh(
        "issue",
        "close",
        str(hit["number"]),
        "--comment",
        "对应文件已从仓库移除，Issue 自动关闭。",
    )
    if result.returncode != 0:
        print(f"  关闭失败 {title}：{result.stderr.strip()}")
        return "failed", False
    print(f"  关闭 #{hit['number']} {title}")
    return "closed", True


def main():
    added = read_lines(ADDED_FILE)
    deleted = read_lines(DELETED_FILE)

    if not added and not deleted:
        print("没有需要处理的 Markdown 变更。")
        return 0

    index = build_issue_index()
    print(f"现有 Issue {len(index)} 条（按标题精确去重）\n")

    counters = {"created": 0, "updated": 0, "closed": 0, "skipped": 0, "failed": 0}

    for path in added:
        if not os.path.isfile(path):
            print(f"跳过不存在的文件：{path}")
            continue
        print(path)
        action, _ = sync_one(path, index)
        counters[action] += 1

    for path in deleted:
        action, _ = close_one(path, index)
        counters[action] += 1

    print(
        "\n汇总：新建 {created}｜更新 {updated}｜关闭 {closed}｜"
        "跳过 {skipped}｜失败 {failed}".format(**counters)
    )
    return 1 if counters["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
