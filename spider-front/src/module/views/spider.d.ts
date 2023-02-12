/**
 # @Time : 2023/1/28 14:49
 # @Site : https://www.codeminer.cn
 """
 file-name:spider
 ex:interface
 """
 */
type domain = 'creation_date' | 'domain_name' | 'emails' | 'expiration_date' | 'name' | 'registrar'
type domainResponseAble = Record<domain, string>
// interface domainResponseAble {
//   creation_date: string
//   domain_name: string
//   emails: string
//   expiration_date: string
//   name: string
//   registrar: string
//
// }

interface spiderResponseAble {
  domain: domainResponseAble, // 域名消息
  imgList: Array<string> // 图片
}

type spiderResponseOptionAble = Partial<spiderResponseAble>
