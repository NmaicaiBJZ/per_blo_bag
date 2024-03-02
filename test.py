from email.parser import Parser  
from email.message import Message  
from io import BytesIO  
  
# 假设你收到的原始数据存储在`raw_data`变量中  
raw_data = b"""  
------WebKitFormBoundaryabc123  
Content-Disposition: form-data; name="field1"  
  
value1  
------WebKitFormBoundaryabc123  
Content-Disposition: form-data; name="field2"  
  
value2  
------WebKitFormBoundaryabc123--  
"""  
  
# 创建一个BytesIO对象，以便像处理文件一样处理原始数据  
data_stream = BytesIO(raw_data)  
  
# 创建一个解析器对象  
parser = Parser()  
  
# 解析数据  
message = parser.parse(data_stream)  
  
# 遍历解析后的parts  
for part in message.walk():  
    # 跳过顶层消息，它只包含子部分  
    if part.get_content_maintype() != 'multipart':  
        # 获取表单字段的名称  
        field_name = part.get('Content-Disposition', {}).get('name')  
        # 获取表单字段的值，并解码为字符串（如果需要）  
        field_value = part.get_payload(decode=True)  
        if isinstance(field_value, bytes):  
            field_value = field_value.decode('utf-8')  
        print(f'Field: {field_name}, Value: {field_value}')  
  
# 输出：  
# Field: field1, Value: value1  
# Field: field2, Value: value2