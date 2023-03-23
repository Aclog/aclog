import os
import pandas as pd
from sqlalchemy import create_engine


# 连接数据库函数
def engine(db_name):
    engine = create_engine('mysql+pymysql://root:root@localhost/{}'.format(db_name))
    return engine


# 创建csv文件
def readFile_to_sql(db_name):
    try:
        # 获取当前路径
        cwd = os.getcwd()
        # 遍历当前路径,路径,文件全部爬去出来
        for dirpaths, dirnaames, filenames in os.walk(cwd):
            # dirpaths路径，dirnaames文件夹的名字，filenames所有文件的名字
            # 判断csv文件是否存在

            for filename in filenames:
                if filename.endswith(".csv"):
                    # 读取文件
                    print(filename)
                    filepath = dirpaths + '\\' + filename
                    print("文件路径"+filepath)
                    df = pd.read_csv(filepath)
                    table_name = filename.split('_')[0]+'_'+filename.split('_')[2]
                    table_name = table_name.split('.')[0]
                    table_name=table_name.lower()
                    # 直接写入数据库,'table_name'为表名,会自动创建一个表,不需要自己动手创建
                    # to_sql函数支持两类mysql引擎一个是sqlalchemy，另一个是sqlliet3,在写入库的时候，pymysql(python3), mysqldb(python2)是不能用的，只能使用sqlalchemy或者sqlliet3.
                    print("表名"+table_name)
                    df.to_sql(table_name, con=engine(db_name), if_exists='append', index=True)



                    # 第一个参数't_pandasRead'是需要导入的表名
                    # 第二个参数数据库引擎
                    # 第三个参数if_exists=""，引号里面可以跟三个参数，fail（如果表存在，啥也不做），replace（如果表存在，删了表，再建立一个新表，把数据插入），append（如果表存在，把数据插入，如果表不存在创建一个表）
                    # 第四个参数是否需要配置索引

    except Exception as e:
        # 输出报错问题
        raise e

