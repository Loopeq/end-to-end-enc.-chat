interface ImportMetaEnv { 
    readonly VITE_API_URL: string
    readonly VITE_WS_URL: string
    readonly GIPHY_API: string
}

interface ImportMeta { 
    readonly env: ImportMetaEnv,
    hot,
}