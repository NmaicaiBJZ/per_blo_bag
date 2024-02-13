# marked.js 使用手册
- 通过 CDN（内容分发网络）引入：
```html
<script src="https://cdn.jsdelivr.net/npm/marked@2.1.3/marked.min.js"></script>
```
- 通过 npm 安装，并在项目中引入：
```bash
npm install marked
```
在你的 JavaScript 文件中引入：
```js
const marked = require('marked');
```
## 简单使用
```js
// 获取 Markdown 文本
const markdownText = '# Hello, marked.js!';
// 使用 marked.js 转换为 HTML
const htmlOutput = marked(markdownText);
// 将 HTML 输出插入到页面中
document.getElementById('output').innerHTML = htmlOutput;
```
## marked.js 配置选项
`marked.parse(markdownString [,options])`
- markdownString: 需要编译的字符串
- options: 设置 marked.use 的全局选项

选项解释：

|成员|类型|解释|默认选项|
|:--|:--|:--|:--:|
|gfm|`boolean`|启用 `GitHub` 风格的 `Markdown`|true|
|breaks|`boolean`|在单个换行符 `(\n)` 上添加 `<br>`<br> 需要启用 `gfm` 选项|false|
|pedantic|`boolean`|尽可能地兼容 `markdown.pl` 的晦涩部分。<br>不纠正原始模型任何的不良行为和错误。<br>关闭并覆盖 `gfm` |false|
|renderer|`object`|渲染选项允许你以自定义的方式渲染内容，并把之前的规则设置覆盖掉。|`new Renderer()`|
|silent|`boolean`|如果为true，则解析器不会抛出任何异常或记录任何警告。任何错误都将作为字符串返回。|false|
|tokenizer|`object`|包含从markdown创建标记的函数。|new Tokenizer()|


