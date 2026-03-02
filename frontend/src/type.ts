
export interface UserAuth {
    username: string
    password: string
}
 
export interface User extends UserAuth { 
    id: string
}

export interface Conversation {
    id: string 
    partner: User
}

export interface Message {
    message: string
    to?: string
    from?: string
}

