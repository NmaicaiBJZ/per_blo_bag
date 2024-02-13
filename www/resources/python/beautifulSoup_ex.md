# BeautifulSoup 模块

BeautifulSoup是一个可以从HTML或XML文件中提取数据的python库；它能够通过转换器实现惯用的文档导航、查找、修改文档的方式。

BeautifulSoup是一个基于re开发的解析库，可以提供一些强大的解析功能；使用BeautifulSoup能够提高提取数据的效率与爬虫开发效率。

## 文档对象

- tag : 标签 eg.`soup.tag`
- Navigable String : 可遍历字符串 eg. `soup.tag.string`
- BeautifulSoup : 文档全部内容 可以当作 tag 对象使用
- Comment : 标签内字符串的注释  eg. `soup.tag.string` 

## 遍历

向下遍历：

- tag.contents : tag标签子节点
- tag.children : tag标签子节点，用于循环遍历子节点
- tag.descendants : tag标签子孙节点，用于循环遍历子孙节点
- tag.parent : tag标签父节点
- tag.parents : tag标签先辈节点，用于循环遍历先别节点

平行遍历：

- tag.next_sibling : tag标签下一兄弟节点
- tag.previous_sibling : tag标签上一兄弟节点
- tag.next_siblings : tag标签后续全部兄弟节点
- tag.previous_siblings : tag标签前序全部兄弟节点

```py
# 向上遍历
print(soup.p.parent.name,'\n')
for i in soup.p.parents:
    print(i.name)

# body 

# body
# html
```

## 搜索文档

- soup.find_all( ) : 查找所有符合条件的标签，返回列表数据
- soup.find : 查找符合条件的第一个个标签，返回字符串数据
- soup.tag.find_parents() : 检索tag标签所有先辈节点，返回列表数据
- soup.tag.find_parent() : 检索tag标签父节点，返回字符串数据
- soup.tag.find_next_siblings() : 检索tag标签所有后续节点，返回列表数据
- soup.tag.find_next_sibling() : 检索tag标签下一节点，返回字符串数据
- soup.tag.find_previous_siblings() : 检索tag标签所有前序节点，返回列表数据
- soup.tag.find_previous_sibling() : 检索tag标签上一节点，返回字符串数据


```python
print(soup.find_all('a'))  #检索标签名
print(soup.find_all('a',id='link1')) #检索属性值
print(soup.find_all('a',class_='sister')) 
print(soup.find_all(text=['Elsie','Lacie']))

# 向上检索
print(soup.p.find_parent().name)
for i in soup.title.find_parents():
    print(i.name)
```

## css 选择器

在Tag或BeautifulSoup对象的.select( )方法中传入字符串参数，即可使用CSS选择器找到Tag。

```python
print('标签查找:',soup.select('a'))
print('属性查找:',soup.select('a[id="link1"]'))
print('类名查找:',soup.select('.sister'))
print('id查找:',soup.select('#link1'))
print('组合查找:',soup.select('p #link1'))
```

## 参考
- [BeautifulSoup（HTML解析）](https://zhuanlan.zhihu.com/p/394268763)