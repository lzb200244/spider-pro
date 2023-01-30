/**
 # @Time : 2023/1/20 22:14
 # @Site : https://www.codeminer.cn
 """
 file-name:data
 ex:
 """
 */
export type NavItem={
  path: string,
  text: string,
  icon: string,
  class?: string,
}

export interface Nav {
  [index: number]: NavItem
}
