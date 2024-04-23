import { Suspense } from "solid-js"
import {
	RouteSectionProps,
	createAsync,
	redirect,
	useAction,
	action,
	cache,
	reload
} from "@solidjs/router"
import { Meta } from "@solidjs/meta"
import Header from "./components/Header"
import Footer from "./components/Footer"
import Grid from "./components/Grid"
import Image from "./components/Image"
import Search from "./components/Search"
import api from "./lib/api"
import { BASE_API_URL } from "./lib/constant"
import shuffleIcon from "./assets/shuffle.svg"

export const getHome = cache(async () => await api.home(), "home")

export const getImages = cache(
	async (image) => await api.images(image),
	"image"
)

export const getSearch = cache(
	async (query) => await api.search(query),
	"search"
)

const shuffle = action(async () => {
	if (location.pathname === "/") {
		await reload({ revalidate: getHome.keyFor() })
	} else {
		throw redirect("/")
	}
})

export const HomePage = () => {
	const images = createAsync(() => getHome())
	return <Grid images={images()} />
}

export const SearchPage = (props: RouteSectionProps) => {
	const query = new URLSearchParams(props.location.search).get("query")
	const images = createAsync(() => getSearch(query))
	return <Grid images={images()} />
}

export const ImagePage = (props: RouteSectionProps) => {
	const images = createAsync(() => getImages(props.params.image))
	const image = `${BASE_API_URL}/${props.params.image}`
	return (
		<>
			<Meta property="og:image" content={image} />
			<Meta name="twitter:image:src" content={image} />
			<Image page={true} id={props.params.image} />
			<Suspense>
				<Grid images={images()} />
			</Suspense>
		</>
	)
}

const App = (props: RouteSectionProps) => {
	const count = createAsync(api.count)
	const onShuffle = useAction(shuffle)

	return (
		<>
			<Header>
				<Search count={count()} />
				<button onClick={onShuffle}>
					<img src={shuffleIcon} />
				</button>
			</Header>
			{props.children}
			<Footer />
		</>
	)
}
export default App
