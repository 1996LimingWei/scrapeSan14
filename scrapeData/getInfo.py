import requests
from bs4 import BeautifulSoup
import csv

def getGeneralInfo():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    url = "https://wikiwiki.jp/sangokushi14/%E5%8F%B2%E5%AE%9F%E6%AD%A6%E5%B0%86%28PK%E3%83%BB%E3%82%BD%E3%83%BC%E3%83%88%E5%8F%AF%29"

    try:
        # 发送请求时携带请求头
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功，如果失败则抛出异常

        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # 先定位包含表格的外层div
        wrapper_div = soup.find('div', class_='wikiwiki-tablesorter-wrapper')
        if wrapper_div:
            # 找到包含表格的div后，再找到里面的table元素
            h_scrollable_div = wrapper_div.find('div', class_='h-scrollable')
            if h_scrollable_div:
                table = h_scrollable_div.find('table')
                
                if table:
                    # 将table的内容输出到txt文件
                    # with open('table_content.txt', 'w', encoding='utf-8') as file:
                    #     file.write(str(table))

                    data = []
                    # 定位表头所在的 tr 标签，通过 thead 来定位
                    thead = table.find('thead')
                    if thead:
                        #print(str(thead).split('\n')[:2])
                        header_row = thead.find('tr')
                        if header_row:
                            # 提取表头信息
                            headers = [th.find('strong').text.strip() for th in header_row.find_all('td')]
                            #print(f"表头数量: {len(headers)}, 表头内容: {headers}")

                            for row in table.find_all('tr')[1:]:
                                cells = row.find_all('td')
                                print(f"当前行单元格数量: {len(cells)}")
                                # 检查单元格数量是否和表头数量一致
                                if len(cells) != len(headers):
                                    print(f"警告: 当前行单元格数量和表头数量不匹配，跳过该行。单元格内容: {[cell.text.strip() for cell in cells]}")
                                    continue
                                row_data = {headers[i]: cells[i].text.strip() for i in range(len(headers))}
                                #print(str(row_data).split('\n')[:2])
                                data.append(row_data)
                            # 某些应用程序在读取 UTF - 8 编码的文件时，需要文件开头有 BOM 才能正确识别编码。我们需要在打开 CSV 文件时指定写入 BOM
                            with open('sanguo_heroes.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
                                fieldnames = headers
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writeheader()
                                for row in data:
                                    writer.writerow(row)
                            return data
                        else:
                            print("未找到表头行")
                    else:
                        print("未找到 thead 元素")
                else:
                    print("未找到table元素")
            else:
                print("未找到包含table的div元素")
        else:
            print("未找到包含表格的外层div元素")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP 错误发生: {http_err}')
    except Exception as err:
        print(f'其他错误发生: {err}')
    return []