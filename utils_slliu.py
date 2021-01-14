# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


# 将一个列表套列表的对象展开（展开嵌套列表）
def flat(nums):
    res = []
    for i in nums:
        if isinstance(i, list):
            res.extend(flat(i))
        else:
            res.append(i)
    return res

# 创建目录，如果目录不存在则创建，如果目录存在则不做任何操作
def mkdir(outdir):
    try:
        os.mkdir(outdir)
    except:
        pass


# 从文件中读取表型结构数据
def read_data(fpath):
    if fpath.endswith('gz'):
        try:
            df = pd.read_excel(fpath,compression='gzip')
        except:
            df = pd.read_csv(fpath, sep='\t',compression='gzip')
    else:
        try:
            df = pd.read_excel(fpath)
        except:
            df = pd.read_csv(fpath, sep='\t')
    # 这个是什么意思？
    dica = {}
    for key in df.keys():
        dica[key] =str(key)
    if dica:
        df.rename(columns=dica,inplace=True)
    return df

# 获取目录下的所有文件（包括子目录的文件）
def walks(path_dir, #文件夹路径
          file_name, # 要搜索的文件名
          fileend, # 要搜索的文件后缀名
          ):
    import os
    file_path = []
    a = os.walk(path_dir)
    for root, dirs, files in a:
        for name in files:
            if file_name:
                if name == file_name:
                    file_path.append(os.path.join(root, name))
            elif fileend:
                if name.endswith(fileend):
                    file_path.append(os.path.join(root, name))
            else:
                file_path.append(os.path.join(root, name))
    return file_path


# 将路径里面的不合法字符替换为合法字符
def path_remake(path):
    return path.replace(' ', '\ ').replace('(','\(').replace(')','\)').replace('&','\&')

# 将pdf文件合并到一起
def merge_pdf_file(pdf_list_join=None, # 待合并的文件列表
                   pdf_dir=None, # 待合并的文件所在的文件夹路径
                   out_path_file_name='merged_pdf.pdf' # 生成的文件的路径和名称
                   ):
    # 待合并文件列表
    pdf_merge_list = []
    # 如果pdf_list_join中有文件
        # 判断是否为列表，如何不为列表则抛出错误
    if isinstance(pdf_list_join, list):
        for item in pdf_list_join:
            item = path_remake(item)
            if os.path.split(item)[-1].endswith('.pdf'):
                pdf_merge_list.append(item)
    else:
        raise("'pdf_list_join' must be a list!!!!!")
    # 如果存在pdf_dir，则遍历其中的pdf文件，
        # 否则抛出文件不存在的错误
    if os.access(pdf_dir, os.F_OK):
        temp_list = walks(pdf_dir, None, '.pdf')
        for item in temp_list:
            item = path_remake(item)
            if os.path.split(item)[-1].endswith('.pdf'):
                pdf_merge_list.append(item)
    else:
        raise (f"{pdf_dir} not exist!!!!!")
    if not pdf_merge_list:
        os.system(f'gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile={out_path_file_name} -f {pdf_merge_list}')

#############################################
# 绘图函数区 start
def draw_pie(labels=None, # 每份数据的标签
             quants=None, # 数据组成的列表
             title_name="未知标题", # 饼图的标题
             colors=None, # 显示的颜色列表，循环显示列表
             highlight=None, # 突出显示
             deviation_distance=0.1# 突出显示的块离圆心的距离
             ):
    # make a square figure
    if quants is None:
        quants = []
    if len(labels) != len(quants):
        raise Exception("quants和labels列表长度不相同！")
    # 如何自定义图片的大小，根据数据大小自适应？？？？？？
    plt.figure(1, figsize=(6,6))
    # 将图分多少份；
    split_pie_num = len(quants)
    # 如何创建一个初始值为0的大小为split_pie_num的列表
    expl = [0 for item in range(split_pie_num)]
    # 如何找到那个分组的数最大，及其下标
    import heapq
    highlight = highlight if highlight else 0
    for item in range(highlight):
        max_index = list(map(quants.index, heapq.nlargest(3, quants)))[item]
        expl[max_index] = deviation_distance

    # Colors used. Recycle if not enough.
    colors  = colors if colors else ["blue","red","coral","green","yellow","orange"]  #设置颜色（循环显示）
    # Pie Plot
    # autopct: format of "percent" string;百分数格式
    plt.pie(quants, explode=expl, colors=colors, labels=labels, autopct='%1.1f%%',pctdistance=0.8, shadow=True)
    plt.title(title_name, bbox={'facecolor':'0.8', 'pad':5})
    plt.show()
    plt.savefig("pie.jpg")
    plt.close()
# 绘图函数区 end
###########################################################
# 对table型文件的处理函数区 start
# 将列表转化为以tab分割的字符串
def list_to_line(column_list):
    column_list = (str(item) for item in column_list)
    return '\t'.join(column_list)

# 将以tab分割的字符串(一般是从文件中读取的一行）转化为列表
def line_to_list(line):
    return line.strip().split('\t')

# 对dataframe按照列字段进行去重
def drop_duplicates(df, colums_name=None):
    if colums_name is None:
        return df.drop_duplicates()
    else:
        return df.drop_duplicates(subset=colums_name,keep='first',inplace=False)

# 将dataframe对象写到文件中
def df_to_tsv(df, file_name=None):
    if file_name is None:
        file_name = 'default.tsv'
    df.to_csv(file_name, sep='\t', header=True, index=False)

# 将dataframe对象写到文件中
def df_to_excel(df, file_name=None, sheet_name=None):
    if file_name is None:
        file_name = 'default.exls'
    if sheet_name is None:
        sheet_name = "sheet1"
    df.to_csv(file_name, sheet_name=sheet_name, index=False)

# 多个dataframe对象写到一个excel文件中，
def dfs_to_one_excel(df_list=None, # dataframe列表
                     sheet_list=None, # 表单列表名称
                     excel_name=None, # 输出的excel文件名
                     df_sheet_map=None # [（df，sheet_name), ...]
                     ):
    if excel_name is None:
        excel_name = "default.exls"
    if df_sheet_map is not None:
        # 检查数据格式
        if isinstance(df_sheet_map, list):
            for item in df_sheet_map:
                isinstance(item, (list, tuple))
        else:
            print("df_sheet_map格式错误：需要有(df,sheet_nem)形式的元素组成的列表；")
        return
    else:
        if df_list is not None:
            if sheet_list is not None:
                if isinstance(df_list, (list, tuple))  and isinstance(sheet_list, (list, tuple)):
                    df_sheet_map = zip(df_list,sheet_list)
            else:
                if isinstance(df_list, list) or isinstance(df_list, tuple):
                    sheet_list = [ "sheet"+str(i) for i in range(len(df_list))]
                    df_sheet_map = list(zip(df_list,sheet_list))
        else:
            print("请传入dataframe对象列表！")
            return
    with pd.ExcelWriter(excel_name) as writer:
        for df, sheet_name in df_sheet_map:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

# 将一个列表形式的表格结构数据转化为dataframe数据结构
def listTable_to_df(listTable, # 表格[[],]
                    header=None, # 表格的第一行为columns
                    columns=None, # 表格的第一行为columns
                    ):
    if header==1:
        title_name = listTable[0]
        list_table = listTable[1:]
        return pd.DataFrame(list_table, columns=title_name)
    else:
        title_name = columns
        list_table = listTable
        return pd.DataFrame(list_table, columns=title_name)


# file_name = "TCGA_COSMIC_merge16Ex_raw_zero37_2.txt"
#
# df = pd.read_csv(file_name, sep="\t")
# df2 = df.head(10)
# series_list = []
# for i, row in df2.iterrows():
#     print(i)
#     print(type(row))
#     row["Gene Name"] = "aaa"
#     series_list.append(row)
# df3 = pd.DataFrame(series_list)
# df3.to_excel("test.xlsx", index=False)


# 对dataframe数据类型进行逐行迭代，对行数据进行操作后在将数据已dataframe数格式返回
def handle_data_by_row_df(df, # dataframe数据格式
                          handle_func # 行数据处理函数，接受一个series格式数据，并返回修改后的数据
                          ):
    series_list = []
    for i, row in df.iterrows():
        row = handle_func(row)
        series_list.append(row)
    df_out = pd.DataFrame(series_list)
    return df_out
######################################
# 工具函数测试区
if __name__ == '__main__':
    labels   = ['USA', 'China', 'test']
    quants   = [15094025.0, 11299967.0, 11299967.0 ]
    title_name = 'usa china pie'
    # colors = ['green', 'yellow']
    colors = ['#BBFFFF', '#EE6363','#9400D3']
    draw_pie(labels=labels,
             quants=quants,
             title_name=title_name,
             colors=colors,
             highlight=1)




