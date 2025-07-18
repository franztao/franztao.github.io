import os

import pandas as pd
import requests
import html2text

# 配置请求头模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def transfer(src, dst):
    # 下载网页
    # url = "https://example.com"  # 替换为目标网址
    url = src
    # url=r'http://cpi.chinapost.com.cn/html1/appreciationstamp/24101/7426-1.htm'
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
        return
        # exit()
    print(response.apparent_encoding)
    # 转换HTML为Markdown
    converter = html2text.HTML2Text()
    converter.ignore_links = True  # 保留链接
    converter.ignore_images = True  # 保留图片
    converter.bypass_tables = False  # 转换表格
    # print(response.content.decode(response.apparent_encoding))
    markdown_content = converter.handle(response.content.decode(response.apparent_encoding))
    # print(markdown_content)
    # 保存结果到Markdown文件
    output_file = dst
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"转换成功！已保存至: {output_file}")
    except IOError as e:
        print(f"文件保存失败: {e}")


src = r'http://cpi.chinapost.com.cn/html1/appreciationstamp/24101/{}-1.htm'
# 5659
dst = r'C:\Users\m01216.METAX-TECH\Desktop\code\franztao.github.io\dst_nolink'

if __name__ == '__main__':
    dstt=r'C:\Users\m01216.METAX-TECH\Desktop\code\franztao.github.io\dstt'
    os.makedirs(dstt,exist_ok=True)
    os.makedirs(dst,exist_ok=True)
    lens=[]
    texts=[]
    for i in range(5660, 7427):
    # for i in range(5660, 5661):
        url = src.format(str(i))
        # print(url)
        path = os.path.join(dst, str(i) + ".md")
        # transfer(url, path)
        if not os.path.exists(path):
            continue
        with open(path,"r",encoding="utf-8") as f:
            text=f.read()
            # ts=text.split("6333-1.htm) >\n[邮票赏析]",)
            ts=text.split("首页 > 集邮信息 > 邮票赏析 > ",)

            text=ts[1]
            # print(
            #     text
            # )
            ts = text.split("\n设计师\n", )
            text = ts[0]
            text=text.replace("下载\n","").replace("\n\n","\n")
            lens.append(len(text))
            # print(
            #     text
            # )
            # with open(os.path.join(dstt, str(i) + ".md"), "w", encoding="utf-8") as f:
            #     f.write(text)
            texts.append(text[0:4000])

    with open(os.path.join(r'C:\Users\m01216.METAX-TECH\Desktop\code\franztao.github.io',   "all.md"), "w", encoding="utf-8") as f:
        f.write('\n#######################################\n'.join(texts))
        # break
        # transfer(url, path)
    df=pd.DataFrame({"l":lens})
    print(df.describe())