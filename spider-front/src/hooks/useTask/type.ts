export interface Time {
  // 时间
  time: string | number | Date,
  // 周几
  num?: number
}

interface Circle extends Time {
  type: 'daily' | 'weekly' | 'monthly' | 'single'
}

export interface Timer<T extends Time> {
  type: string,
  timer: T
}
