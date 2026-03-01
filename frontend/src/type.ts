
export interface UserAuth {
    username: string
    password: string
}
 
export interface User extends UserAuth { 
    id: string
}

export interface Conversation { 
    user1_id: User['id']
    user2_id: User['id']
}

export interface Message {
    username: string
    message: string
}

