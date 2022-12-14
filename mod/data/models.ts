export type Base = {
  id: number
  created_at: Date
}

export type State = "draft" | "started" | "ended" | "locked" | "greenlit"

export type Campaign = Base & {
  campaigner_id: number

  title: string
  description: string
  challenges: string
  cover_id: number | null

  goal: number
  pledged: number
  deadline: Date

  current_state: State
}

export type Access = "banned" | "normal" | "mod" | "admin"

export type User = Base & {
  name: string
  email: string

  about: string | null
  contact: string | null
  address: string | null
  portrait_id: number | null

  access_level: Access
}

export type Image = Base & {
  uploader_id: number

  filename: string
  filetype: string
  location: string
}

export type Reportable = "user" | "campaign" | "reply"

export type Report = Base & {
  reporter_id: number

  description: string

  content_id: number
  content_type: Reportable
}

export type TokenData = {
  access_token: string
  token_type: string
  access_level: Access
}

export type LoginData = {
  username: string
  password: string
}

export const columns = {
  supers: {
    current: "current",
    ban: "ban",
    mod: "mod",
  },
  campaigns: {
    ended: "ended",
    greenlit: "greenlit",
    locked: "locked",
  },
  reports: {
    recents: "recents",
    dismiss: "dismiss",
  },
}

