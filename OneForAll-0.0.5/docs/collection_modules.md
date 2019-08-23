#  收集模块说明 #

如果要使用通过API收集子域的模块请先到[config.py](../oneforall/config.py)配置相关信息，大多平台的API都是可以注册账号免费获取的。

如果你指定使用某些模块可以在[config.py](../oneforall/config.py)中设置：

```python
enable_all_module = False  # 不开启所有模块
enable_partial_module = [('modules.search', 'ask')，('modules.search', 'baidu')]  # 只使用ask和baidu搜索引擎收集子域
```

如果你指定使用某些模块使用代理可以在[config.py](../oneforall/config.py)中设置：

```python
enable_proxy = True  # 使用代理
proxy_all_module = False  # 不代理所有模块
proxy_partial_module = ['GoogleQuery', 'AskSearch']  # 只代理GoogleQuery和AskSearch模块（各个模块的source属性值）
```

以下是各个模块说明：

 1. 利用证书透明度收集子域（目前有6个模块：`censys_api`，`certdb_api`，`certspotter`，`crtsh`，`entrust`，`google`）
    
      | 模块名称    | 是否需要代理 | 是否需要API | 其他说明                                           |
      | ----------- | ------------ | ----------- | -------------------------------------------------- |
      | censys_api  | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | certdb_api  | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | certspotter | 否           | 否          |                                                    |
      | crtsh       | 否           | 否          |                                                    |
      | entrust     | 否           | 否          |                                                    |
      | google      | 是           | 否          |                                                    |


  2. 常规检查收集子域（目前有4个模块：域传送漏洞利用`axfr`，检查跨域策略文件`cdx`，检查HTTPS证书`cert`，检查内容安全策略`csp`，后续会添加检查NSEC记录，NSEC3记录等模块）

      | 模块名称 | 是否需要代理           | 是否需要API | 其他说明           |
      | -------- | ---------------------- | ----------- | ------------------ |
      | axfr     | 否                     | 否          | 域传送漏洞利用     |
      | cdx      | 手动设置（默认不使用） | 否          | 检查跨域策略文件   |
      | cert     | 否                     | 否          | 检查HTTPS证书      |
      | csp      | 手动设置（默认不使用） | 否          | 检查内容安全策略   |
      | robots   | 手动设置（默认不使用） | 否          | 检查robots.txt文件 |
      | sitemap  | 手动设置（默认不使用） | 否          | 检查sitemap文件    |
  3. 利用网上爬虫档案收集子域（目前有2个模块：`archivecrawl`，`commoncrawl`，此模块还在调试，该模块还有待添加和完善）

      | 模块名称     | 是否需要代理 | 是否需要API | 其他说明 |
      | ------------ | ------------ | ----------- | -------- |
      | archivecrawl | 否           | 否          |          |
      | commoncrawl  | 否           | 否          |          |

  4. 利用DNS数据集收集子域（目前有17个模块：`binaryedge_api`, `circl_api`, `hackertarget`, `riddler`, `bufferover`, `dnsdb`, `ipv4info`, `robtex`, `chinaz`, `dnsdb_api`, `netcraft`, `securitytrails_api`, `chinaz_api`, `dnsdumpster`, `ptrarchive`, `sitedossier`,`threatcrowd`）

      | 模块名称           | 是否需要代理 | 是否需要API | 其他说明                                           |
      | ------------------ | ------------ | ----------- | -------------------------------------------------- |
      | binaryedge_api     | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | bufferover         | 否           | 否          |                                                    |
      | chinaz             | 否           | 否          |                                                    |
      | chinaz_api         | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | circl_api          | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | dnsdb              | 否           | 否          |                                                    |
      | dnsdb_api          | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | dnsdumpster        | 否           | 否          |                                                    |
      | hackertarget       | 否           | 否          |                                                    |
      | ipv4info           | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | netcraft           | 否           | 否          |                                                    |
      | ptrarchive         | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | riddler            | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | robtex             | 否           | 否          |                                                    |
      | securitytrails_api | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | sitedossier        | 否           | 否          |                                                    |
      | threatcrowd        | 否           | 否          |                                                    |
  5. 利用DNS查询收集子域（目前有1个模块：通过枚举常见的SRV记录并做查询来收集子域`srv`，该模块还有待添加和完善）

      | 模块名称 | 是否需要代理 | 是否需要API | 其他说明                      |
      | -------- | ------------ | ----------- | ----------------------------- |
      | srv      | 否           | 否          | 枚举域名常见的SRV记录发现子域 |
  6. 利用威胁平台数据收集子域（目前有5个模块：`riskiq_api`，`threatbook_api`，`threatminer`，`virustotal`，`virustotal_api`该模块还有待添加和完善）

      | 模块名称       | 是否需要代理 | 是否需要API | 其他说明                                           |
      | -------------- | ------------ | ----------- | -------------------------------------------------- |
      | riskiq_api     | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | threatbook_api | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
      | threatminer    | 否           | 否          |                                                    |
      | virustotal     | 否           | 否          |                                                    |
      | virustotal_api | 否           | 是          | API使用和申请见[config.py](../oneforall/config.py) |
  7. 利用搜索引擎发现子域（目前有15个模块：`ask`, `bing_api`, `fofa_api`, `shodan_api`, `yahoo`, `baidu`, `duckduckgo`, `google`, `so`, `yandex`, `bing`, `exalead`, `google_api`, `sogou`, `zoomeye_api`）

     除特殊搜索引擎，通用的搜索引擎都支持自动排除搜索，全量搜索，递归搜索。

     | 模块        | 是否需要代理           | 是否需要API | 其他说明                                           |
     | ----------- | ---------------------- | ----------- | -------------------------------------------------- |
     | ask         | 是                     | 否          |                                                    |
     | baidu       | 否                     | 否          |                                                    |
     | bing        | 否                     | 否          |                                                    |
     | bing_api    | 否                     | 是          | API使用和申请见[config.py](../oneforall/config.py) |
     | duckduckgo  | 是                     | 否          |                                                    |
     | exalead     | 否，最好使用国外代理。 | 否          |                                                    |
     | fofa_api    | 否                     | 是          | API使用和申请见[config.py](../oneforall/config.py) |
     | google      | 是                     | 否          |                                                    |
     | google_api  | 是                     | 是          | API使用和申请见[config.py](../oneforall/config.py) |
     | shodan_api  | 否，最好使用国外代理。 | 是          | API使用和申请见[config.py](../oneforall/config.py) |
     | so          | 否                     | 否          |                                                    |
     | sogou       | 否                     | 否          |                                                    |
     | yahoo       | 是                     | 否          |                                                    |
     | yandex      | 是                     | 否          |                                                    |
     | zoomeye_api | 否                     | 是          | API使用和申请见[config.py](../oneforall/config.py) |