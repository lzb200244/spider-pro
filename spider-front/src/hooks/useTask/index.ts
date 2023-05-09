import { reactive } from 'vue'
import { Timer, Time } from '@/hooks/useTask/type'
export function useTask<T extends Time>() {
  const timer = reactive<Timer<T>>({ type: 'single', timer: {} as T })

  return { timer }
}
