type domain = 'creation_date' | 'domain_name' | 'emails' | 'expiration_date' | 'name' | 'registrar'
export type domainResponseAble = Record<domain, string>

export interface spiderResponseAble {
  domain: domainResponseAble, // 域名消息
  imgList: Array<string> // 图片
}

export type spiderResponseOptionAble = Partial<spiderResponseAble>

export interface spiderDomainAble {

  url: string,
  opt: string[],
  type:string,
  mode: boolean,
  static: boolean,
  email?: string,
  name?: string,
  time?: string,
  customOptions?: any[]
}
