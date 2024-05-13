import { BASE_API_URL } from "./constant"

const count = async () => {
    const response = await fetch(`${BASE_API_URL}/count`, {
        headers: {
            'Accept': 'application/json'
        }
    })
    const data = await response.json()
    return data.count
}

const home = async () => {
    const response = await fetch(BASE_API_URL, {
        headers: {
            'Accept': 'application/json'
        }
    })
    return await response.json()
}

const images = async (image: string) => {
    const response = await fetch(`${BASE_API_URL}/${image}`, {
        headers: {
            'Accept': 'application/json'
        }
    })
    return await response.json()
}

const search = async (query: string) => {
    const response = await fetch(`${BASE_API_URL}/search?query=${query}`, {
        headers: {
            'Accept': 'application/json'
        }
    })
    return await response.json()
}

export default {
    count,
    home,
    images,
    search
}