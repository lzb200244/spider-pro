/**
 # @Time : 2023/1/31 17:16
 # @Site : https://www.codeminer.cn
 """
 file-name:type.d.ts
 ex:
 """
 */
type NavItem={
  path: string,
  text: string,
  icon: string,
  class?: string,
}

interface Nav {
  [index: number]: NavItem
}
