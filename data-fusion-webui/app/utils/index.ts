import type { AvatarProps } from '@nuxt/ui'
import type { Member } from '~/types'
import type { PlatformUser } from '~/types/platform'

export function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

export function randomFrom<T>(array: T[]): T {
  return array[Math.floor(Math.random() * array.length)]!
}

export function platformUserToMember(user: PlatformUser): Member {
  const firstName = user.first_name?.trim() ?? ''
  const lastName = user.last_name?.trim() ?? ''
  const fullName = [firstName, lastName].filter(Boolean).join(' ') || user.email
  const initialsSource = [firstName, lastName].map((part) => part.charAt(0)).filter(Boolean).join('')
  const initials = (initialsSource || user.email.charAt(0) || '?').toUpperCase()

  const avatar: AvatarProps = {
    text: initials
  }

  return {
    name: fullName,
    username: user.email,
    role: 'member',
    avatar
  }
}
