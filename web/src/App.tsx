import { RouteSectionProps, createAsync, useParams } from "@solidjs/router"
import { Meta } from "@solidjs/meta"
import Header from "./components/Header"
import Footer from "./components/Footer"
import Grid from "./components/Grid"
import Image from "./components/Image"
import { BASE_API_URL } from "./lib/constant"

const fetchCount = async () => {
	const response = await fetch(`${BASE_API_URL}/count`)
	return await response.json()
}

const fetchHomeImages = async () => {
	const response = await fetch(BASE_API_URL)
	return await response.json()
}

const fetchImages = async () => {
	const params = useParams()
	const response = await fetch(`${BASE_API_URL}/${params.image}`)
	return await response.json()
}

export const HomePage = () => {
	const images = createAsync(fetchHomeImages)
	return <Grid images={images()} />
}

export const ImagePage = () => {
	const params = useParams()
	const images = createAsync(fetchImages)
	const image = `${BASE_API_URL}/${params.image}`
	return (
		<>
			<Meta property="og:image" content={image} />
			<Meta name="twitter:image:src" content={image} />
			<Image page={true} id={params.image} />
			<Grid images={images()} />
		</>
	)
}

const App = (props: RouteSectionProps) => {
	return (
		<>
			<Header />
			{props.children}
			<Footer />
		</>
	)
}
export default App
