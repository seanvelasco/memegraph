import { BASE_API_URL } from "./constant"

const count = async () => {
    const response = await fetch(`${BASE_API_URL}/count`)
    const data = await response.json()
    return data.count
}

const home = async () => {
    const response = await fetch(BASE_API_URL)
    return await response.json()
}

const images = async (image: string) => {
    const response = await fetch(`${BASE_API_URL}/${image}`)
    return await response.json()
}

const search = async (query: string) => {
    const response = await fetch(`${BASE_API_URL}/search?query=${query}`)
    return await response.json()
}

export default {
    count,
    home,
    images,
    search
}