/**
 # @Time : 2023/1/28 14:49
 # @Site : https://www.codeminer.cn
 """
 file-name:spider
 ex:interface
 """
 */

interface spiderResponseAble {
  domain: object, // 域名消息
  imgList: Array<string> // 图片
}

export interface domainResponseAble{
  creation_date:string
  domain_name:string
  emails:string
  expiration_date:string
  name:string
  registrar:string

}
export type spiderResponseOptionAble = Partial<spiderResponseAble>
