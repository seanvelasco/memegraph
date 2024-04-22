import { RouteSectionProps, createAsync, useParams } from "@solidjs/router"
import { Meta } from "@solidjs/meta"
import Header from "./components/Header"
import Footer from "./components/Footer"
import Grid from "./components/Grid"
import Image from "./components/Image"

const fetchHomeImages = async () => {
	const response = await fetch(import.meta.env.API_URL)
	return await response.json()
}

const fetchImages = async () => {
	const params = useParams()
	const response = await fetch(`${import.meta.env.API_URL}/${params.image}`)
	return await response.json()
}

export const HomePage = () => {
	const images = createAsync(fetchHomeImages)
	return <Grid images={images()} />
}

export const ImagePage = () => {
	const params = useParams()
	const images = createAsync(fetchImages)
	const image = `${import.meta.env.API_URL}/${params.image}`
	return (
		<>
			<Meta property="og:image" content={image} />
			<Meta name="twitter:image:src" content={image} />
			<Image page={true} id={params.image} />
			<Grid images={images()} />
		</>
	)
}

const App = (props: RouteSectionProps) => (
	<>
		<Header />
		{props.children}
		<Footer />
	</>
)

export default App
