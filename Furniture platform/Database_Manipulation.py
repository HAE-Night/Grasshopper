import sqlite3


class Database_Manipulation:

    def __init__(self):
        self.conn = sqlite3.connect("db.sqlite3")  # 连接数据库

    def Select_Max_ID(self):
        cur = self.conn.cursor()  # 创建游标
        sql_query = "select max(ID) from Products_products"
        cur.execute(sql_query)
        return cur.fetchall()[0][0]

    def Insert_ALLData(self, List_result, start_index, list_img_index, price_strategy, inquiry_code):
        cur = self.conn.cursor()  # 创建游标

        for result_index, result in enumerate(List_result):  # 遍历结果列表
            if any(result):
                result_photo_index = str(result_index + start_index + 1)
                print(result_index)
                if result_photo_index in list_img_index:
                    Item_Photo_path = "Photos/" + result_photo_index + '.png'
                else:
                    Item_Photo_path = None
                result += (Item_Photo_path, inquiry_code)  # 打印结果
                cur.execute(
                    "INSERT INTO Products_products ('CATEGORY', 'ROOM_AREA', 'ITEM', "
                    "'DESCRIPTION', 'SIZE_DIMENSION', 'LENGTH_MM', 'WIDTH_MM', 'HEIGHT_MM','QTY','UNIT','UNIT_PRICE_AED','ITEM_PHOTO','INQUIRY_CODE') "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    result)  # 执行插入操作，将结果作为参数传入
        self.conn.commit()  # 提交事务

    def Update(self):
        pass

    def Delete(self):
        pass


if __name__ == '__main__':
    x = Database_Manipulation()
    print(x.Select_Max_ID())
